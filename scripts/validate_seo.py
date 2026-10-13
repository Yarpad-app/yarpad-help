#!/usr/bin/env python3
"""Validate SEO artifacts in a built MkDocs site using the standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


SITE_URL = "https://help.yarpad.app/"
SITEMAP_URL = "https://help.yarpad.app/sitemap.xml"
SUPPORTED_SCHEMA_TYPES = frozenset({"WebPage", "WebSite", "TechArticle"})
CANONICAL_PATTERN = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', re.IGNORECASE
)
TITLE_PATTERN = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DESCRIPTION_PATTERN = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)',
    re.IGNORECASE,
)
META_PATTERN = re.compile(
    r'<meta\s+(?:property|name)=["\']([^"\']+)["\']\s+content=["\']([^"\']*)',
    re.IGNORECASE,
)
JSON_LD_PATTERN = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


class SeoValidationError(ValueError):
    """Raised when a required SEO artifact is invalid."""


def _content_pages(site_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in site_dir.rglob("index.html")
        if path.name == "index.html" and path.parent.name != "404"
    )


def _metadata(page: Path) -> tuple[str, str, str, dict[str, str]]:
    content = page.read_text(encoding="utf-8")
    title_match = TITLE_PATTERN.search(content)
    description_match = DESCRIPTION_PATTERN.search(content)
    canonical_match = CANONICAL_PATTERN.search(content)
    if not title_match or not title_match.group(1).strip():
        raise SeoValidationError(f"missing title: {page}")
    if not description_match or not description_match.group(1).strip():
        raise SeoValidationError(f"missing description: {page}")
    if not canonical_match:
        raise SeoValidationError(f"missing canonical URL: {page}")
    canonical = canonical_match.group(1).strip()
    parsed = urlparse(canonical)
    if parsed.scheme != "https" or parsed.netloc != "help.yarpad.app":
        raise SeoValidationError(f"canonical URL is outside site_url: {page}: {canonical}")
    metadata = {name: value for name, value in META_PATTERN.findall(content)}
    if metadata.get("og:title") != title_match.group(1).strip():
        raise SeoValidationError(f"SEO title is not the document title: {page}")
    if metadata.get("og:description") != description_match.group(1).strip():
        raise SeoValidationError(f"SEO description is not the document description: {page}")
    return title_match.group(1).strip(), description_match.group(1).strip(), canonical, metadata


def _validate_social_metadata(
    page: Path,
    seo_title: str,
    description: str,
    canonical: str,
    metadata: dict[str, str],
    has_social_image: bool,
) -> None:
    expected_type = "website" if canonical == SITE_URL else "article"
    expected = {
        "og:title": seo_title,
        "og:description": description,
        "og:url": canonical,
        "og:type": expected_type,
        "twitter:card": "summary",
        "twitter:title": seo_title,
        "twitter:description": description,
    }
    for name, value in expected.items():
        if metadata.get(name) != value:
            raise SeoValidationError(f"invalid {name} metadata: {page}")
    image_names = ("og:image", "twitter:image")
    if has_social_image:
        expected_image = f"{SITE_URL}assets/social-preview.png"
        for name in image_names:
            if metadata.get(name) != expected_image:
                raise SeoValidationError(f"invalid {name} metadata: {page}")
    elif any(name in metadata for name in image_names):
        raise SeoValidationError(f"social image metadata references a missing asset: {page}")


def _validate_json_ld(
    page: Path,
    title: str,
    description: str,
    canonical: str,
    expected_type: str,
) -> None:
    content = page.read_text(encoding="utf-8")
    blocks = JSON_LD_PATTERN.findall(content)
    if len(blocks) != 1:
        raise SeoValidationError(f"expected exactly one JSON-LD entity: {page}")
    try:
        entity = json.loads(blocks[0])
    except json.JSONDecodeError as error:
        raise SeoValidationError(f"invalid JSON-LD syntax: {page}: {error}") from error
    if not isinstance(entity, dict):
        raise SeoValidationError(f"JSON-LD entity must be an object: {page}")
    if entity.get("@type") not in SUPPORTED_SCHEMA_TYPES:
        raise SeoValidationError(f"unsupported JSON-LD type: {page}")
    expected = {
        "@context": "https://schema.org",
        "@type": expected_type,
        "name": title,
        "description": description,
        "url": canonical,
        "inLanguage": "en",
    }
    for key, value in expected.items():
        if entity.get(key) != value:
            raise SeoValidationError(f"invalid JSON-LD {key}: {page}")
    fabricated_keys = {
        "author",
        "datePublished",
        "dateModified",
        "aggregateRating",
        "review",
        "faq",
        "step",
    }
    if fabricated_keys.intersection(entity):
        raise SeoValidationError(f"JSON-LD contains unverified metadata: {page}")


def _sitemap_urls(site_dir: Path) -> set[str]:
    sitemap = site_dir / "sitemap.xml"
    if not sitemap.is_file():
        raise SeoValidationError("site/sitemap.xml is missing")
    try:
        root = ET.parse(sitemap).getroot()
    except ET.ParseError as error:
        raise SeoValidationError(f"invalid sitemap.xml: {error}") from error
    urls = {
        element.text.strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text
    }
    if not urls:
        raise SeoValidationError("sitemap.xml contains no URLs")
    if any(not url.startswith(SITE_URL) for url in urls):
        raise SeoValidationError("sitemap.xml contains a URL outside site_url")
    if len(urls) != len(
        [element for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "loc"]
    ):
        raise SeoValidationError("sitemap.xml contains duplicate URLs")
    if any("/investigate/" in url for url in urls):
        raise SeoValidationError("sitemap.xml publishes an investigation page")
    return urls


def _validate_robots(site_dir: Path) -> None:
    robots = site_dir / "robots.txt"
    if not robots.is_file():
        raise SeoValidationError("site/robots.txt is missing")
    content = robots.read_text(encoding="utf-8")
    if "User-agent: *" not in content or "Allow: /" not in content:
        raise SeoValidationError("robots.txt does not allow public indexing")
    if SITEMAP_URL not in content:
        raise SeoValidationError("robots.txt does not reference the canonical sitemap")


def validate_site(site_dir: Path) -> None:
    if not site_dir.is_dir():
        raise SeoValidationError(f"site directory is missing: {site_dir}")
    pages = _content_pages(site_dir)
    if not pages:
        raise SeoValidationError("no published HTML pages found")
    metadata = [_metadata(page) for page in pages]
    titles = [item[0] for item in metadata]
    descriptions = [item[1] for item in metadata]
    canonicals = {item[2] for item in metadata}
    if len(canonicals) != len(metadata):
        raise SeoValidationError("published page canonical URLs are not unique")
    if len(titles) != len(set(titles)):
        raise SeoValidationError("published page titles are not unique")
    if len(descriptions) != len(set(descriptions)):
        raise SeoValidationError("published page descriptions are not unique")
    seo_titles = [item[3].get("og:title", "").strip() for item in metadata]
    if any(not title for title in seo_titles):
        raise SeoValidationError("published page SEO titles are missing")
    if len(seo_titles) != len(set(seo_titles)):
        raise SeoValidationError("published page SEO titles are not unique")
    if any("/investigate/" in str(page.relative_to(site_dir)) for page in pages):
        raise SeoValidationError("an investigation page is in the published output")
    has_social_image = (site_dir / "assets" / "social-preview.png").is_file()
    for page, (title, description, canonical, page_metadata), seo_title in zip(
        pages, metadata, seo_titles
    ):
        _validate_social_metadata(
            page,
            seo_title,
            description,
            canonical,
            page_metadata,
            has_social_image,
        )
        expected_type = _json_ld_type(page)
        _validate_json_ld(page, seo_title, description, canonical, expected_type)
    sitemap_urls = _sitemap_urls(site_dir)
    if sitemap_urls != canonicals:
        raise SeoValidationError("sitemap URLs do not match page canonical URLs")
    _validate_robots(site_dir)
    cname = site_dir / "CNAME"
    if not cname.is_file() or cname.read_text(encoding="utf-8").strip() != "help.yarpad.app":
        raise SeoValidationError("CNAME is missing or does not preserve help.yarpad.app")


def _json_ld_type(page: Path) -> str:
    """Read the schema type emitted by MkDocs without knowing page paths."""

    content = page.read_text(encoding="utf-8")
    blocks = JSON_LD_PATTERN.findall(content)
    if len(blocks) != 1:
        raise SeoValidationError(f"expected exactly one JSON-LD entity: {page}")
    try:
        entity = json.loads(blocks[0])
    except json.JSONDecodeError as error:
        raise SeoValidationError(f"invalid JSON-LD syntax: {page}: {error}") from error
    schema_type = entity.get("@type") if isinstance(entity, dict) else None
    if schema_type not in SUPPORTED_SCHEMA_TYPES:
        raise SeoValidationError(f"unsupported JSON-LD type: {page}")
    return schema_type


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    args = parser.parse_args(argv)
    try:
        validate_site(args.site_dir)
    except (OSError, SeoValidationError) as error:
        print(f"SEO validation failed: {error}", file=sys.stderr)
        return 1
    print(f"SEO validation passed for {args.site_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
