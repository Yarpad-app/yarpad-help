"""MkDocs build hooks for normalized, metadata-driven SEO."""

from pathlib import Path
import os

SUPPORTED_SCHEMA_TYPES = frozenset({"WebPage", "WebSite", "TechArticle"})


def on_page_markdown(markdown, page, config, files):
    """Normalize the metadata shared by every SEO output format."""

    metadata = dict(page.meta or {})
    default_title = config.site_name if page.is_homepage else page.title
    seo_title = str(metadata.get("seo_title") or default_title or "").strip()
    description = str(
        metadata.get("seo_description") or metadata.get("description") or config.site_description
    ).strip()
    schema_type = str(metadata.get("schema_type") or "WebPage").strip()
    if not seo_title:
        raise ValueError(f"published page has no SEO title: {page.file.src_path}")
    if not description:
        raise ValueError(f"published page has no SEO description: {page.file.src_path}")
    if schema_type not in SUPPORTED_SCHEMA_TYPES:
        supported = ", ".join(sorted(SUPPORTED_SCHEMA_TYPES))
        raise ValueError(
            f"unsupported schema_type {schema_type!r} on {page.file.src_path}; "
            f"expected one of: {supported}"
        )

    canonical_url = f"{config.site_url.rstrip('/')}/{page.url}"
    metadata.update(
        {
            "seo_title": seo_title,
            "seo_description": description,
            "description": description,
            "canonical_url": canonical_url,
            "schema_type": schema_type,
            "social_type": "website" if page.is_homepage else "article",
        }
    )
    page.meta = metadata
    page.canonical_url = canonical_url
    return markdown


def on_config(config):
    """Expose the social preview image only when the asset exists."""

    image = Path(config.docs_dir) / "assets" / "social-preview.png"
    extra = dict(config.extra)
    extra["social_preview_image"] = "assets/social-preview.png" if image.is_file() else None
    configured_verification = extra.get("google_site_verification")
    environment_verification = os.environ.get("GOOGLE_SITE_VERIFICATION", "").strip()
    extra["google_site_verification"] = environment_verification or configured_verification or None
    config.extra = extra
    return config
