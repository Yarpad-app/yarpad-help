from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.mkdocs_hooks import on_page_markdown
from scripts.validate_seo import validate_site


def write_site(
    root: Path,
    include_image: bool = False,
    bad_og_url: bool = False,
    additional_pages: dict[str, tuple[str, str, str, str]] | None = None,
) -> None:
    pages = {
        "index.html": ("Yarpad Help Center", "Yarpad help for teachers and students.", "website", "", "WebSite"),
        "guide/index.html": ("Teacher Guide", "Teacher account guidance.", "article", "guide/", "TechArticle"),
        "legal/index.html": ("Terms of Service", "Current Yarpad Terms of Service.", "article", "legal/", "WebPage"),
    }
    for relative, values in (additional_pages or {}).items():
        pages[relative] = (*values, "WebPage")
    for relative, (title, description, social_type, path, schema_type) in pages.items():
        (root / relative).parent.mkdir(parents=True, exist_ok=True)
        canonical = f"https://help.yarpad.app/{path}"
        og_url = "https://help.yarpad.app/wrong/" if bad_og_url and path else canonical
        social_title = title
        image_metadata = (
            '<meta property="og:image" content="https://help.yarpad.app/assets/social-preview.png">'
            '<meta name="twitter:image" content="https://help.yarpad.app/assets/social-preview.png">'
            if include_image
            else ""
        )
        json_ld = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": schema_type,
                "name": social_title,
                "description": description,
                "url": canonical,
                "inLanguage": "en",
            }
        )
        html = f'''<html><head>
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{social_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{og_url}">
<meta property="og:type" content="{social_type}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{social_title}">
<meta name="twitter:description" content="{description}">
{image_metadata}
<script type="application/ld+json">{json_ld}</script>
</head><body><h1>{title}</h1></body></html>'''
        (root / relative).write_text(html, encoding="utf-8")
    (root / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://help.yarpad.app/sitemap.xml\n",
        encoding="utf-8",
    )
    (root / "CNAME").write_text("help.yarpad.app\n", encoding="utf-8")
    sitemap_urls = [f"https://help.yarpad.app/{values[3]}" for values in pages.values()]
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *(f"  <url><loc>{url}</loc></url>" for url in sitemap_urls),
        "</urlset>",
        "",
    ]
    (root / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")
    if include_image:
        image = root / "assets" / "social-preview.png"
        image.parent.mkdir()
        image.write_bytes(b"not-a-real-image-fixture")


class SeoValidationTests(unittest.TestCase):
    def test_temporary_documentation_page_gets_complete_seo_metadata(self):
        repository = Path(__file__).resolve().parents[1]
        seo_sources = {
            repository / "scripts" / "mkdocs_hooks.py": (
                repository / "scripts" / "mkdocs_hooks.py"
            ).read_bytes(),
            repository / "overrides" / "main.html": (
                repository / "overrides" / "main.html"
            ).read_bytes(),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text(
                "---\n"
                "seo_title: Temporary Yarpad Help Center\n"
                "description: Temporary Yarpad Help Center home.\n"
                "schema_type: WebSite\n"
                "---\n\n"
                "# Temporary Home\n",
                encoding="utf-8",
            )
            (docs / "new-topic.md").write_text(
                "---\n"
                "seo_title: New Topic for Yarpad Users\n"
                "description: Guidance for a newly published Yarpad topic.\n"
                "schema_type: TechArticle\n"
                "---\n\n"
                "# New Topic\n\n"
                "This page was added without SEO code changes.\n",
                encoding="utf-8",
            )
            (docs / "robots.txt").write_text(
                "User-agent: *\nAllow: /\n\n"
                "Sitemap: https://help.yarpad.app/sitemap.xml\n",
                encoding="utf-8",
            )
            (docs / "CNAME").write_text("help.yarpad.app\n", encoding="utf-8")
            config = root / "mkdocs.yml"
            config.write_text(
                f"site_name: Yarpad Help Center\n"
                f"site_url: https://help.yarpad.app/\n"
                f"docs_dir: {docs}\n"
                f"use_directory_urls: true\n"
                f"hooks:\n  - {repository / 'scripts' / 'mkdocs_hooks.py'}\n"
                "nav:\n"
                "  - Home: index.md\n"
                "  - New Topic: new-topic.md\n"
                "theme:\n"
                "  name: material\n"
                f"  custom_dir: {repository / 'overrides'}\n"
                "plugins:\n  - search\n",
                encoding="utf-8",
            )
            site = root / "site"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "mkdocs",
                    "build",
                    "--strict",
                    "--config-file",
                    str(config),
                    "--site-dir",
                    str(site),
                ],
                cwd=repository,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            validate_site(site)
            for source, before in seo_sources.items():
                self.assertEqual(source.read_bytes(), before)
            generated = next(
                page.read_text(encoding="utf-8")
                for page in sorted(site.rglob("index.html"))
                if "New Topic for Yarpad Users" in page.read_text(encoding="utf-8")
            )
            for marker in (
                'property="og:title"',
                'property="og:description"',
                'property="og:url"',
                'property="og:type"',
                'name="twitter:card"',
                'name="twitter:title"',
                'name="twitter:description"',
                'rel="canonical"',
                'application/ld+json',
            ):
                self.assertIn(marker, generated)
            self.assertIn("<title>New Topic for Yarpad Users</title>", generated)

    def test_new_published_page_uses_metadata_without_path_specific_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            write_site(
                site,
                additional_pages={
                    "new-topic/index.html": (
                        "New Topic",
                        "A newly published Yarpad topic.",
                        "article",
                        "new-topic/",
                    )
                },
            )
            validate_site(site)

    def test_mkdocs_metadata_defaults_schema_type_for_new_pages(self):
        page = type(
            "Page",
            (),
            {
                "title": "New Topic",
                "is_homepage": False,
                "url": "new-topic/",
                "meta": {"description": "A newly published Yarpad topic."},
                "file": type("File", (), {"src_path": "new-topic.md"})(),
            },
        )()
        config = type(
            "Config",
            (),
            {
                "site_name": "Yarpad Help Center",
                "site_description": "Default description.",
                "site_url": "https://help.yarpad.app/",
            },
        )()

        on_page_markdown("# New Topic", page, config, [])

        self.assertEqual(page.meta["seo_title"], "New Topic")
        self.assertEqual(page.meta["seo_description"], "A newly published Yarpad topic.")
        self.assertEqual(page.meta["schema_type"], "WebPage")
        self.assertEqual(page.meta["canonical_url"], "https://help.yarpad.app/new-topic/")

    def test_mkdocs_metadata_rejects_unsupported_schema_type(self):
        page = type(
            "Page",
            (),
            {
                "title": "New Topic",
                "is_homepage": False,
                "url": "new-topic/",
                "meta": {
                    "description": "A newly published Yarpad topic.",
                    "schema_type": "HowTo",
                },
                "file": type("File", (), {"src_path": "new-topic.md"})(),
            },
        )()
        config = type(
            "Config",
            (),
            {
                "site_name": "Yarpad Help Center",
                "site_description": "Default description.",
                "site_url": "https://help.yarpad.app/",
            },
        )()

        with self.assertRaisesRegex(ValueError, "unsupported schema_type"):
            on_page_markdown("# New Topic", page, config, [])

    def test_social_metadata_and_canonical_urls_are_valid_without_image(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            write_site(site)
            validate_site(site)

    def test_mismatched_og_url_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            write_site(site, bad_og_url=True)
            with self.assertRaises(ValueError):
                validate_site(site)

    def test_existing_social_image_requires_absolute_image_urls(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            write_site(site, include_image=True)
            validate_site(site)

    def test_fabricated_json_ld_metadata_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            write_site(site)
            guide = next(
                page for page in site.rglob("index.html") if page != site / "index.html"
            )
            content = guide.read_text(encoding="utf-8")
            content = content.replace(
                '"inLanguage": "en"',
                '"author": {"name": "Unknown"}, "inLanguage": "en"',
            )
            guide.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_site(site)

    def test_unsupported_json_ld_type_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            write_site(site)
            home = site / "index.html"
            content = home.read_text(encoding="utf-8").replace('"@type": "WebSite"', '"@type": "HowTo"')
            home.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_site(site)


if __name__ == "__main__":
    unittest.main()
