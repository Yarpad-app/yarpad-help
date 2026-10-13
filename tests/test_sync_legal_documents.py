import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError
from urllib.request import Request, build_opener

from scripts.sync_legal_documents import (
    DEFAULT_TERMS_URL,
    DocumentSpec,
    _NoRedirect,
    SyncError,
    fetch_json,
    render_markdown,
    synchronize,
    validate_document,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "legal"
SPECS = (
    DocumentSpec("terms", "Terms of Service", DEFAULT_TERMS_URL, "terms-of-service.md"),
    DocumentSpec("policy", "Privacy Policy", "https://yarpad.app/api/v1/publish/policy", "privacy-policy.md"),
)


def fixture(name):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class LegalSynchronizationTests(unittest.TestCase):
    def test_valid_terms_and_policy_generate_deterministic_complete_pages(self):
        payloads = {spec.key: fixture(f"{spec.key}.json") for spec in SPECS}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "legal"
            first = synchronize(SPECS, output, lambda spec: payloads[spec.key])
            first_bytes = {
                path.name: path.read_bytes() for path in output.iterdir()
            }
            second = synchronize(SPECS, output, lambda spec: payloads[spec.key])
            second_bytes = {
                path.name: path.read_bytes() for path in output.iterdir()
            }

        self.assertEqual(first, second)
        self.assertEqual(first_bytes, second_bytes)
        terms = first_bytes["terms-of-service.md"].decode("utf-8")
        self.assertIn("test-1.0", terms)
        self.assertIn("Effective Date:</strong> January 15, 2026", terms)
        self.assertIn("https://yarpad.app/help", terms)
        self.assertNotIn("<style", terms)
        self.assertNotIn("style=", terms)

    def test_unsafe_html_and_links_are_rejected(self):
        payload = fixture("terms.json")
        payload["content"] = payload["content"].replace(
            "<h1>", "<script>alert(1)</script><h1>"
        )
        with self.assertRaises(SyncError):
            validate_document(SPECS[0], payload)

        payload = fixture("terms.json")
        payload["content"] = payload["content"].replace(
            "https://yarpad.app/help", "javascript:alert(1)"
        )
        with self.assertRaises(SyncError):
            validate_document(SPECS[0], payload)

    def test_missing_or_malformed_fields_are_rejected(self):
        for field in ("version", "language", "title", "content"):
            payload = fixture("terms.json")
            payload.pop(field)
            with self.subTest(field=field), self.assertRaises(SyncError):
                validate_document(SPECS[0], payload)

        payload = fixture("terms.json")
        payload["language"] = "FA"
        with self.assertRaises(SyncError):
            validate_document(SPECS[0], payload)

        payload = fixture("terms.json")
        payload["content"] = "<p>No effective date</p>"
        with self.assertRaises(SyncError):
            validate_document(SPECS[0], payload)

    def test_network_failure_is_reported(self):
        def failing_opener(request, timeout):
            raise URLError("offline")

        opener = type("Opener", (), {"open": staticmethod(failing_opener)})()
        with self.assertRaises(SyncError), patch(
            "scripts.sync_legal_documents.build_opener",
            return_value=opener,
        ):
            fetch_json(DEFAULT_TERMS_URL)

    def test_custom_redirect_handler_is_accepted_by_urllib(self):
        handler = _NoRedirect()
        opener = build_opener(handler)
        self.assertIn(handler, opener.handlers)

    def test_http_redirects_are_rejected(self):
        handler = _NoRedirect()
        request = Request(DEFAULT_TERMS_URL)
        for status in (301, 302):
            with self.subTest(status=status), self.assertRaises(SyncError):
                handler.redirect_request(
                    request,
                    None,
                    status,
                    "redirect",
                    {},
                    "https://yarpad.app/redirected",
                )

    def test_partial_validation_failure_leaves_existing_output_unchanged(self):
        payloads = {spec.key: fixture(f"{spec.key}.json") for spec in SPECS}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "legal"
            synchronize(SPECS, output, lambda spec: payloads[spec.key])
            before = {path.name: path.read_bytes() for path in output.iterdir()}
            payloads["policy"] = dict(payloads["policy"], language="FA")

            with self.assertRaises(SyncError):
                synchronize(SPECS, output, lambda spec: payloads[spec.key])

            after = {path.name: path.read_bytes() for path in output.iterdir()}
        self.assertEqual(before, after)

    def test_partial_network_failure_leaves_existing_output_unchanged(self):
        payloads = {spec.key: fixture(f"{spec.key}.json") for spec in SPECS}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "legal"
            synchronize(SPECS, output, lambda spec: payloads[spec.key])
            before = {path.name: path.read_bytes() for path in output.iterdir()}

            def fail_for_policy(spec):
                if spec.key == "policy":
                    raise SyncError("policy request failed")
                return payloads[spec.key]

            with self.assertRaises(SyncError):
                synchronize(SPECS, output, fail_for_policy)

            after = {path.name: path.read_bytes() for path in output.iterdir()}
        self.assertEqual(before, after)

    def test_rendered_page_is_markdown_with_sanitized_html(self):
        document = validate_document(SPECS[1], fixture("policy.json"))
        rendered = render_markdown(document)
        self.assertTrue(rendered.startswith("<!-- Generated"))
        self.assertIn('<div class="yarpad-legal-document">', rendered)
        self.assertIn("<h2>1. Contact</h2>", rendered)


if __name__ == "__main__":
    unittest.main()
