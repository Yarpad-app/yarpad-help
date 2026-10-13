#!/usr/bin/env python3
"""Synchronize Yarpad legal documents into generated MkDocs pages.

The production API is the source of truth. Fixture mode exists only for
offline pull-request validation.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


DEFAULT_TERMS_URL = "https://yarpad.app/api/v1/publish/terms"
DEFAULT_POLICY_URL = "https://yarpad.app/api/v1/publish/policy"
DEFAULT_OUTPUT_DIR = Path("docs/legal")
DEFAULT_TIMEOUT_SECONDS = 15.0
DEFAULT_MAX_RESPONSE_BYTES = 1_000_000
EXPECTED_LANGUAGE = "EN"

ALLOWED_TAGS = {
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "section",
    "span",
    "strong",
    "u",
    "ul",
}
VOID_TAGS = {"br"}
IGNORED_STYLE_TAGS = {"style"}
FORBIDDEN_TAGS = {
    "base",
    "embed",
    "form",
    "iframe",
    "img",
    "input",
    "link",
    "meta",
    "object",
    "script",
    "svg",
    "template",
    "textarea",
    "video",
    "audio",
}
SAFE_SCHEMES = {"http", "https", "mailto"}
VERSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$")
DATE_PATTERN = re.compile(
    r"(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December)\s+\d{1,2},?\s+\d{4}|\d{4}-\d{2}-\d{2}",
    re.IGNORECASE,
)
EFFECTIVE_DATE_PATTERN = re.compile(
    r"effective\s+date\s*:\s*("
    r"(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December)\s+\d{1,2},?\s+\d{4}|\d{4}-\d{2}-\d{2})",
    re.IGNORECASE,
)


class SyncError(ValueError):
    """Raised when a legal document cannot be safely synchronized."""


@dataclass(frozen=True)
class DocumentSpec:
    key: str
    title: str
    url: str
    filename: str


@dataclass(frozen=True)
class LegalDocument:
    spec: DocumentSpec
    version: str
    language: str
    title: str
    content: str
    effective_date: str
    sanitized_html: str


class _NoRedirect(HTTPRedirectHandler):
    """Reject redirects so the configured HTTPS origin is authoritative."""

    def redirect_request(self, request, fp, code, msg, headers, new_url):
        raise SyncError(f"redirect rejected for {request.full_url}")


def _validate_source_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "yarpad.app":
        raise SyncError(f"source URL must use https://yarpad.app: {url}")


def _read_response(response, max_bytes: int) -> bytes:
    content_length = response.headers.get("Content-Length")
    if content_length:
        try:
            if int(content_length) > max_bytes:
                raise SyncError("API response exceeds the configured size limit")
        except ValueError as error:
            raise SyncError("API returned an invalid Content-Length") from error

    body = response.read(max_bytes + 1)
    if len(body) > max_bytes:
        raise SyncError("API response exceeds the configured size limit")
    return body


def fetch_json(
    url: str,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_RESPONSE_BYTES,
    opener: Callable[..., object] | None = None,
) -> dict[str, object]:
    """Fetch and parse one API response with bounded, HTTPS-only input."""

    _validate_source_url(url)
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "yarpad-help-legal-sync/1",
        },
        method="GET",
    )
    open_url = opener or build_opener(_NoRedirect()).open

    try:
        response = open_url(request, timeout=timeout)
        status = getattr(response, "status", None)
        if status is None:
            status = response.getcode()
        if status != 200:
            raise SyncError(f"API returned HTTP {status}")
        content_type = response.headers.get("Content-Type", "")
        if content_type and "json" not in content_type.lower():
            raise SyncError("API response is not JSON")
        body = _read_response(response, max_bytes)
    except HTTPError as error:
        raise SyncError(f"API request failed with HTTP {error.code}") from error
    except (URLError, TimeoutError, OSError) as error:
        raise SyncError(f"API request failed: {error.reason if isinstance(error, URLError) else error}") from error

    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SyncError("API response is not valid UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise SyncError("API response must be a JSON object")
    return payload


class _Sanitizer:
    def __init__(self) -> None:
        self.output: list[str] = []
        self.text_parts: list[str] = []
        self.stack: list[str] = []
        self.style_depth = 0

    def _location(self) -> str:
        return " > ".join(self.stack) or "document root"

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if self.style_depth:
            if tag == "style":
                self.style_depth += 1
            return
        if tag in IGNORED_STYLE_TAGS:
            self.style_depth = 1
            return
        if tag in FORBIDDEN_TAGS:
            raise SyncError(f"unsupported active HTML element: <{tag}>")
        if tag not in ALLOWED_TAGS:
            raise SyncError(f"unsupported HTML element: <{tag}>")

        clean_attrs: list[tuple[str, str]] = []
        for name, value in attrs:
            name = name.lower()
            if name.startswith("on"):
                raise SyncError(f"event handler attribute is not allowed: {name}")
            if name == "style":
                continue
            if tag in {"div", "section"} and name == "class":
                # Source classes are presentation-only. The generated wrapper
                # supplies the reviewed legal-document scope.
                continue
            if tag == "a" and name == "href":
                if value is None or not _safe_href(value):
                    raise SyncError("unsafe or empty legal-document link")
                clean_attrs.append(("href", value))
                continue
            if tag == "a" and name == "title":
                if value is not None:
                    clean_attrs.append(("title", value))
                continue
            raise SyncError(f"unsupported attribute on <{tag}>: {name}")

        if tag == "a" and not any(name == "href" for name, _ in clean_attrs):
            raise SyncError("legal-document links must have an href")

        attr_text = "".join(
            f' {name}="{html.escape(value, quote=True)}"'
            for name, value in clean_attrs
        )
        self.output.append(f"<{tag}{attr_text}>")
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.style_depth:
            if tag == "style":
                self.style_depth -= 1
            return
        if tag not in ALLOWED_TAGS:
            raise SyncError(f"unsupported HTML closing element: </{tag}>")
        if tag in VOID_TAGS:
            raise SyncError(f"unexpected closing element: </{tag}>")
        if not self.stack or self.stack[-1] != tag:
            raise SyncError(f"unbalanced HTML near {self._location()}")
        self.stack.pop()
        self.output.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self.style_depth:
            return
        self.output.append(html.escape(data, quote=False))
        self.text_parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.style_depth:
            return
        value = html.unescape(f"&{name};")
        self.output.append(f"&{name};")
        self.text_parts.append(value)

    def handle_charref(self, name: str) -> None:
        if self.style_depth:
            return
        value = html.unescape(f"&#{name};")
        self.output.append(f"&#{name};")
        self.text_parts.append(value)

    def handle_comment(self, data: str) -> None:
        raise SyncError("HTML comments are not allowed in legal content")

    def handle_decl(self, decl: str) -> None:
        raise SyncError("HTML declarations are not allowed in legal content")

    def finish(self) -> tuple[str, str]:
        if self.style_depth:
            raise SyncError("unclosed <style> element")
        if self.stack:
            raise SyncError(f"unclosed HTML element: <{self.stack[-1]}>")
        sanitized = "".join(self.output).strip()
        visible_text = "".join(self.text_parts)
        if not sanitized or not visible_text.strip():
            raise SyncError("legal HTML content is empty")
        return sanitized, visible_text


def _safe_href(href: str) -> bool:
    value = html.unescape(href).strip()
    if not value or any(ord(char) < 0x20 for char in value):
        return False
    if value.startswith("//"):
        return False
    parsed = urlparse(value)
    if parsed.scheme and parsed.scheme.lower() not in SAFE_SCHEMES:
        return False
    return True


def sanitize_html(content: str) -> tuple[str, str]:
    if not isinstance(content, str) or not content.strip():
        raise SyncError("content must be a non-empty HTML string")
    from html.parser import HTMLParser

    sanitizer = _Sanitizer()
    parser = HTMLParser(convert_charrefs=False)
    parser.handle_starttag = sanitizer.handle_starttag
    parser.handle_startendtag = sanitizer.handle_startendtag
    parser.handle_endtag = sanitizer.handle_endtag
    parser.handle_data = sanitizer.handle_data
    parser.handle_entityref = sanitizer.handle_entityref
    parser.handle_charref = sanitizer.handle_charref
    parser.handle_comment = sanitizer.handle_comment
    parser.handle_decl = sanitizer.handle_decl
    try:
        parser.feed(content)
        parser.close()
    except SyncError:
        raise
    except Exception as error:
        raise SyncError(f"malformed legal HTML: {error}") from error
    return sanitizer.finish()


def extract_effective_date(visible_text: str) -> str:
    normalized = re.sub(r"\s+", " ", visible_text).strip()
    matches = list(EFFECTIVE_DATE_PATTERN.finditer(normalized))
    if len(matches) != 1:
        raise SyncError("legal HTML must contain exactly one Effective Date")
    candidate = matches[0].group(1).strip()
    date_match = DATE_PATTERN.fullmatch(candidate.rstrip(" ."))
    if not date_match:
        raise SyncError("Effective Date must be a recognized date")
    return date_match.group(0)


def _required_string(payload: dict[str, object], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise SyncError(f"API field {field!r} must be a non-empty string")
    return value.strip()


def validate_document(spec: DocumentSpec, payload: dict[str, object]) -> LegalDocument:
    version = _required_string(payload, "version")
    language = _required_string(payload, "language")
    title = _required_string(payload, "title")
    content = _required_string(payload, "content")
    if not VERSION_PATTERN.fullmatch(version):
        raise SyncError(f"invalid {spec.key} document version")
    if language != EXPECTED_LANGUAGE:
        raise SyncError(f"{spec.key} document language must be {EXPECTED_LANGUAGE}")
    if title.casefold() != spec.title.casefold():
        raise SyncError(f"{spec.key} document title does not match {spec.title!r}")
    sanitized_html, visible_text = sanitize_html(content)
    effective_date = extract_effective_date(visible_text)
    return LegalDocument(
        spec=spec,
        version=version,
        language=language,
        title=title,
        content=content,
        effective_date=effective_date,
        sanitized_html=sanitized_html,
    )


def render_markdown(document: LegalDocument) -> str:
    return (
        "<!-- Generated during the documentation build. Do not edit or commit. -->\n"
        f"**Document version:** `{document.version}`  \n"
        f"**Language:** `{document.language}`  \n"
        f"**Effective date:** {document.effective_date}\n\n"
        '<div class="yarpad-legal-document">\n'
        f"{document.sanitized_html}\n"
        "</div>\n"
    )


def load_fixture(fixture_dir: Path, filename: str) -> dict[str, object]:
    path = fixture_dir / filename
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SyncError(f"fixture not found: {path}") from error
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SyncError(f"invalid fixture {path}: {error}") from error
    if not isinstance(payload, dict):
        raise SyncError(f"fixture must contain a JSON object: {path}")
    return payload


def _write_documents_transactionally(
    output_dir: Path, documents: Iterable[LegalDocument]
) -> None:
    output_dir = output_dir.resolve()
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = output_dir.parent / f".{output_dir.name}.tmp-{uuid.uuid4().hex}"
    backup_dir = output_dir.parent / f".{output_dir.name}.backup-{uuid.uuid4().hex}"
    try:
        temp_dir.mkdir()
        for document in documents:
            with (temp_dir / document.spec.filename).open(
                "w", encoding="utf-8", newline="\n"
            ) as generated_file:
                generated_file.write(render_markdown(document))

        had_existing = output_dir.exists()
        if had_existing:
            os.replace(output_dir, backup_dir)
        try:
            os.replace(temp_dir, output_dir)
        except Exception:
            if had_existing and backup_dir.exists() and not output_dir.exists():
                os.replace(backup_dir, output_dir)
            raise
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
    except Exception:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        if backup_dir.exists() and not output_dir.exists():
            os.replace(backup_dir, output_dir)
        raise


def synchronize(
    specs: tuple[DocumentSpec, DocumentSpec],
    output_dir: Path,
    source_loader: Callable[[DocumentSpec], dict[str, object]],
) -> tuple[LegalDocument, LegalDocument]:
    documents = tuple(validate_document(spec, source_loader(spec)) for spec in specs)
    _write_documents_transactionally(output_dir, documents)
    return documents


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--fixture-dir", type=Path, help="read terms.json and policy.json locally")
    source.add_argument("--production", action="store_true", help="fetch the configured API endpoints")
    parser.set_defaults(production=True)
    parser.add_argument("--terms-url", default=DEFAULT_TERMS_URL)
    parser.add_argument("--policy-url", default=DEFAULT_POLICY_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-response-bytes", type=int, default=DEFAULT_MAX_RESPONSE_BYTES)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.timeout <= 0 or args.max_response_bytes <= 0:
        print("timeout and max-response-bytes must be positive", file=sys.stderr)
        return 2
    specs = (
        DocumentSpec("terms", "Terms of Service", args.terms_url, "terms-of-service.md"),
        DocumentSpec("policy", "Privacy Policy", args.policy_url, "privacy-policy.md"),
    )
    try:
        if args.fixture_dir:
            source_loader = lambda spec: load_fixture(args.fixture_dir, f"{spec.key}.json")
        else:
            source_loader = lambda spec: fetch_json(
                spec.url, timeout=args.timeout, max_bytes=args.max_response_bytes
            )
        documents = synchronize(specs, args.output_dir, source_loader)
    except (SyncError, OSError) as error:
        print(f"legal document synchronization failed: {error}", file=sys.stderr)
        return 1
    print(
        "Synchronized "
        + ", ".join(
            f"{document.spec.key} {document.version} ({document.effective_date})"
            for document in documents
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
