# personal-site

Website for **Ron Systems AI** ([ronsystemsai.com](https://ronsystemsai.com)): IT systems, automation, and AI consulting for small and medium businesses in English-speaking markets, by Rolando "Ron" Tactay.

## Project map

```
personal-site/
├── README.md                     ← you are here
├── PRODUCT.md                    ← one-page product summary (used by design tooling)
├── .gitignore                    ← keeps the resume, secrets, and Python caches out of git
├── app/                          ← Flask app (routes, templates, static, content data)
├── content/                      ← Markdown articles and videos
├── deploy/                       ← Caddy + Compose files for the VPS
├── tests/                        ← pytest
└── docs/                         ← planning: what the site is for and how it will work
    ├── 01-purpose-and-positioning.md
    ├── 02-audience-and-markets.md
    ├── 03-services.md            ← services in plain business language
    ├── 04-site-structure.md      ← sitemap, page templates, content backlog
    ├── 05-search-and-ai-visibility.md  ← SEO / AEO / GEO plan
    ├── 06-social-and-content.md  ← Facebook, YouTube, LinkedIn
    ├── 07-launch-checklist.md    ← domain, legal, payments, proof, tech launch
    ├── 08-open-decisions.md      ← decided + still-open choices
    ├── 09-architecture-and-deployment.md  ← Flask, Docker, VPS, prod/test, CI/CD
    ├── 10-git-workflow.md        ← branches, releases, conventions
    ├── about-ron/                ← private resume (gitignored)
    └── site-initial-design/      ← first design prototype (reference only)
```

## Stack at a glance

Flask + Jinja2 (server-rendered) · plain HTML/CSS/JS · Markdown content · Docker · VPS · Caddy · Umami

| Environment | URL | Branch |
|---|---|---|
| prod | ronsystemsai.com | `main` |
| test | test.ronsystemsai.com | `develop` |

## Run it locally

```bash
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt   # macOS/Linux: .venv/bin/python
.venv/Scripts/python -m flask --app wsgi run --debug          # http://127.0.0.1:5000
.venv/Scripts/python -m pytest -q                             # tests
```

Or with Docker: `docker compose up --build` → http://127.0.0.1:8000

## Where things live

| What | Where |
|---|---|
| Page copy (services, process, FAQs, case studies) | `app/site_content.py` |
| Articles and videos | `content/resources/*.md`, `content/videos/*.md` (see `content/README.md`) |
| Templates | `app/templates/` |
| Styles / scripts | `app/static/css/site.css`, `app/static/js/site.js` |
| SEO: robots, sitemap, llms.txt, structured data | `app/routes/seo.py`, `app/services/schema.py` |
| Settings (Calendly, SMTP, Umami, social links) | environment variables, see `.env.example` |
| Deployment (Caddy, Umami, prod/test) | `deploy/`, `.github/workflows/` |
