# Yarpad Help Center

Public documentation for Yarpad, built with [MkDocs](https://www.mkdocs.org/)
and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

The published site is intended to be available at
<https://help.yarpad.app/>.

## Local development

Create and activate a virtual environment, then install the pinned
documentation dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Preview the site locally with automatic rebuilds:

```bash
mkdocs serve
```

Open the local URL shown by MkDocs, usually <http://127.0.0.1:8000/>.

Build the site exactly as the deployment workflow does:

```bash
mkdocs build --strict
```

The generated files are written to `site/`, which is ignored by Git.

## Deployment

Push changes to the repository's `main` branch, or start the **Deploy
documentation** workflow manually from the GitHub Actions tab. The workflow
builds the site and deploys it through the official GitHub Pages actions.

Before the first deployment, an administrator must configure the repository's
Pages source to **GitHub Actions** in **Settings → Pages**. No credentials or
deployment tokens are stored in this repository.

## Custom domain and DNS

The `docs/CNAME` file is included in the generated site and declares
`help.yarpad.app`. The DNS administrator must add:

- an **A** record for `help.yarpad.app` pointing to GitHub Pages' documented
  IPv4 addresses, or
- an **AAAA** record set if IPv6 is being configured, following GitHub's current
  Pages documentation.

The exact DNS records depend on the DNS provider and should be verified against
the official [GitHub Pages custom domain
documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).
After DNS propagation, the repository administrator must set the custom domain
to `help.yarpad.app` in **Settings → Pages** and enable HTTPS when GitHub makes
it available. DNS, repository settings, and certificate provisioning are not
changed automatically by this project.

## Future languages

English is the initial published language and remains at the root URL without a
language prefix. When translations are approved, localized copies can be added
under `/pl/` and `/fa/`, with English continuing to use the existing stable
URLs. The translation structure, navigation, and language switcher should be
designed and reviewed before publishing those routes.

No translation plugin is installed at this stage. The empty future-content
directories are intentionally excluded from navigation and search until they
contain approved documentation pages.
