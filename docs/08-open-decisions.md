# 08 — Decisions

## Decided (2026-09-30)

| # | Decision | Choice | Notes |
|---|---|---|---|
| 1 | **Brand name** | **Ron Systems AI** | The About page and structured data say "Rolando 'Ron' Tactay" so search engines and AI tools connect the brand to the person. |
| 2 | **Domain** | **ronsystemsai.com** | Showed no DNS records on 2026-09-30, so it looks unregistered. Confirm with a registrar before buying. Matching handles: `@ronsystemsai`. |
| 3 | **Tech stack** | **Flask (Python) + server-rendered HTML (Jinja2) + plain CSS and JavaScript** | No frontend framework, no build step. Server-rendered pages suit search and AI crawlers. See [09-architecture-and-deployment.md](09-architecture-and-deployment.md). |
| 4 | **Hosting** | **Own VPS, Docker containers** | Two environments: **prod** and **test**. See [09-architecture-and-deployment.md](09-architecture-and-deployment.md). |
| 5 | **Git workflow** | **Simple git flow**: `main` → prod, `develop` → test, short-lived feature branches | See [10-git-workflow.md](10-git-workflow.md). |
| 6 | **Pricing on the site** | **Not shown** | Services use "scoped and quoted before work starts" wording. No price figures anywhere on the site. |
| 7 | **Language** | **English**, US spelling | Matches the existing copy ("prioritized"). One variant site-wide. |
| 8 | **Individuals offer** | **Skipped for now** | Site targets small and medium businesses. Revisit later. |
| 9 | **Social channels** | **Facebook, YouTube, LinkedIn** | Same name, one-liner, photo, and link on all three. |
| 10 | **Time zones and availability** | **Not on the site** | No time-zone FAQ and no response-time promise for support. Call slots are managed manually in Calendly. |
| 11 | **Client-location claims** | **Not on the site** | No "Working with clients in AU/NZ/EU/Asia" or "Available to clients in…" lines in the site copy. Target markets stay in hidden metadata only (structured data `areaServed`). |
| 12 | **Analytics** | **Umami (self-hosted on the VPS) + Google Search Console + Bing Webmaster Tools** | Umami: visits, pages, referrers (incl. AI assistants), countries, devices, and events (Book-a-call clicks, form submits, Calendly bookings). Cookie-less, so no consent banner. Search Console and Bing show the search queries. Enabled on prod only. |
| 13 | **Reverse proxy** | **Caddy** | Runs as a container; automatic HTTPS for `ronsystemsai.com`, `www` (redirect), `test.` (basic auth + noindex), and `stats.`. Also sets security headers and compression. See [09-architecture-and-deployment.md](09-architecture-and-deployment.md). |
| 14 | **Email provider** | **Proton Mail**, custom domain `hello@ronsystemsai.com` | Needs a paid plan that supports custom domains. Contact-form mail is sent through **Proton SMTP submission** (`smtp.protonmail.ch:587`, STARTTLS, per-address SMTP token), available only on some paid plans, so confirm before buying. Fallback if your plan lacks it: send form mail through a transactional service (e.g. Amazon SES, Postmark) *to* the Proton inbox. DNS: Proton's verification TXT, MX, SPF, DKIM (3 CNAMEs), and DMARC records. |

All decisions made as of 2026-09-30.
