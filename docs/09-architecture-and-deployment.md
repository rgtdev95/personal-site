# 09 — Architecture and deployment

## Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | **Flask** (Python 3.12) | Familiar, small, and enough for a content site plus a contact form |
| Templates | **Jinja2**, server-rendered | Every page arrives as complete HTML, which search engines and AI crawlers can read without running JavaScript |
| Styling | **Plain CSS** (custom properties / design tokens, no framework) | Full control of the look; no build step |
| Interactivity | **Plain JavaScript**, progressive enhancement only | Content and navigation work without JS; JS adds the diagram animation, process stepper, theme toggle, and mobile menu |
| Content | **Markdown files with front-matter** for articles, videos, and case studies | Writing a new article = adding one `.md` file. No database needed |
| App server | **Gunicorn** inside the container | Production WSGI server |
| Container | **Docker** + **Docker Compose** | Same image runs in test and prod |
| Reverse proxy / TLS | **Caddy** (decided) | Automatic HTTPS certificates, compression, security headers, routes both environments by hostname |
| Hosting | Own **VPS** | Both environments on one VPS to start |
| Analytics | **Umami** (self-hosted container on the same VPS, with its own PostgreSQL) | Cookie-less; served from `stats.ronsystemsai.com` |

No database for launch. Contact-form messages are emailed (and optionally logged to a file). Add SQLite or PostgreSQL only when something actually needs storage.

## Planned project layout

```
personal-site/
├── app/
│   ├── __init__.py            # create_app() factory, loads config by APP_ENV
│   ├── config.py              # BaseConfig / TestConfig / ProductionConfig
│   ├── routes/
│   │   ├── pages.py           # home, services, work, process, about, faq, book, contact, legal
│   │   ├── content.py         # /resources/<slug>, /videos/<slug>, /work/<slug>
│   │   └── seo.py             # sitemap.xml, robots.txt, llms.txt, security.txt
│   ├── services/
│   │   ├── content_loader.py  # reads Markdown + front-matter, caches
│   │   ├── mailer.py          # contact-form email via Proton SMTP submission
│   │   └── schema.py          # builds JSON-LD structured data
│   ├── templates/
│   │   ├── base.html          # <head>, meta, OG tags, JSON-LD, header/footer
│   │   ├── partials/
│   │   └── pages/
│   └── static/
│       ├── css/
│       ├── js/
│       ├── img/
│       └── fonts/             # self-hosted fonts (faster, no third-party requests)
├── content/
│   ├── resources/*.md
│   ├── videos/*.md
│   └── work/*.md
├── tests/                     # pytest: routes return 200, sitemap valid, noindex on test, etc.
├── deploy/
│   ├── Caddyfile
│   ├── compose.proxy.yml    # Caddy (+ Umami)
│   ├── compose.prod.yml
│   └── compose.test.yml
├── Dockerfile
├── compose.yml                # local development
├── requirements.txt
├── .env.example               # documented settings, no secrets
├── .github/workflows/         # CI + deploy (see below)
├── docs/                      # planning (this folder)
│   ├── about-ron/             # private resume, gitignored
│   └── site-initial-design/   # design reference
```

## Environments

| | **test** | **prod** |
|---|---|---|
| URL | `test.ronsystemsai.com` | `ronsystemsai.com` (+ `www` → redirect) |
| Git branch | `develop` | `main` |
| `APP_ENV` | `test` | `production` |
| Search indexing | **Blocked**: `robots.txt` disallows all + `X-Robots-Tag: noindex` header | Allowed, including AI crawlers |
| Access | HTTP basic auth (via Caddy) | Public |
| Contact form | Logs only (or sends to a test address) | Sends via Proton SMTP to `hello@ronsystemsai.com` |
| Analytics (Umami) | Off | On |

⚠️ **Blocking indexing on test is critical.** If Google or AI crawlers index the test site, it becomes duplicate content that competes with the real one.

## How the containers run on the VPS

```
Internet ──► Caddy (ports 80/443, TLS)
               ├── www.ronsystemsai.com    ──► 301 redirect to ronsystemsai.com
               ├── ronsystemsai.com        ──► web-prod  (gunicorn :8000, image :prod-<sha>)
               ├── test.ronsystemsai.com   ──► web-test  (gunicorn :8000, image :test-<sha>)  [basic auth, noindex]
               └── stats.ronsystemsai.com  ──► umami     (:3000) + umami-db (PostgreSQL, internal only)
```

- Caddy runs in its own Compose project (`deploy/compose.proxy.yml`) and owns ports 80/443. It's the only container exposed to the internet.
- Each environment is its own Compose project (`compose.prod.yml`, `compose.test.yml`) on a shared Docker network (`web`) with Caddy. App containers publish no ports on the host.
- Certificates: Caddy gets and renews Let's Encrypt certificates automatically. Keep its `/data` volume so certificates survive restarts. DNS A records for `@`, `www`, `test`, and `stats` all point to the VPS.

### Caddyfile outline

```caddyfile
{
	email hello@ronsystemsai.com
}

(security_headers) {
	header {
		Strict-Transport-Security "max-age=31536000; includeSubDomains"
		X-Content-Type-Options "nosniff"
		Referrer-Policy "strict-origin-when-cross-origin"
		Permissions-Policy "camera=(), microphone=(), geolocation=()"
		-Server
	}
}

www.ronsystemsai.com {
	redir https://ronsystemsai.com{uri} permanent
}

ronsystemsai.com {
	import security_headers
	encode zstd gzip
	reverse_proxy web-prod:8000
}

test.ronsystemsai.com {
	import security_headers
	header X-Robots-Tag "noindex, nofollow"
	basic_auth {
		{$TEST_USER} {$TEST_PASS_HASH}
	}
	encode zstd gzip
	reverse_proxy web-test:8000
}

stats.ronsystemsai.com {
	import security_headers
	encode zstd gzip
	reverse_proxy umami:3000
}
```

The Content-Security-Policy is set per page by Flask, because the booking page needs to allow Calendly and the other pages don't.
- Secrets (Proton SMTP token, `SECRET_KEY`, test-site basic-auth hash) live in `.env.prod` / `.env.test` **on the VPS only**, never in git.
- Containers run as a non-root user, with `restart: unless-stopped` and a `/healthz` endpoint for health checks.

## CI/CD (GitHub Actions)

| Trigger | Steps |
|---|---|
| Pull request to `develop` or `main` | Lint (ruff) → tests (pytest) → build the Docker image (no deploy) |
| Push/merge to `develop` | Tests → build image → push to GitHub Container Registry (GHCR) tagged `test-<sha>` → SSH to VPS → `docker compose -f compose.test.yml pull && up -d` |
| Push/merge to `main` | Tests → build → push `prod-<sha>` → deploy to prod → ping IndexNow with changed URLs |
| Rollback | Redeploy the previous `prod-<sha>` tag |

The GitHub repo holds a deploy SSH key and the VPS host as **repository secrets**. The deploy user on the VPS can only run Docker Compose in the site directory.

## Security and performance baseline

- Security headers: HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy (set in Caddy); Content-Security-Policy (set per page in Flask)
- Contact form: CSRF token, honeypot field, rate limiting (Flask-Limiter), server-side validation
- `/.well-known/security.txt`
- Gzip/zstd compression and long cache headers for static files (cache-busting via file hash in the URL)
- Self-hosted fonts, optimized images (WebP/AVIF), no third-party scripts except Calendly on the booking page
- VPS: firewall (only 22/80/443), SSH keys only, automatic security updates, off-server backups of `.env` files and content
- Uptime monitoring for both URLs

## SEO/AEO/GEO hooks built into the app

- `base.html` renders the title, meta description, canonical URL, and Open Graph tags from each page's data
- `schema.py` produces JSON-LD for Organization/ProfessionalService, Person, Service, FAQPage, Article, VideoObject, and BreadcrumbList
- `seo.py` generates `sitemap.xml` from routes + Markdown content, and serves an environment-aware `robots.txt` and `llms.txt`
- Every Markdown item has `title`, `description`, `published`, `updated`, and `author` in its front-matter

See [05-search-and-ai-visibility.md](05-search-and-ai-visibility.md) for the full plan.
