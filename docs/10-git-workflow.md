# 10 — Git workflow

A simple git flow with two long-lived branches, each tied to an environment.

```
feature/*  ──PR──►  develop  ──PR──►  main
                      │                 │
                      ▼                 ▼
               test.ronsystemsai.com   ronsystemsai.com
                                        ▲
hotfix/*  ──PR──────────────────────────┘  (then merge main back into develop)
```

## Branches

| Branch | Purpose | Deploys to | Rules |
|---|---|---|---|
| `main` | What's live | **prod** | Protected. Changes only via PR from `develop` or `hotfix/*`. Tagged on each release. |
| `develop` | Integration; what's being tested | **test** | Protected. Changes via PR from `feature/*` / `fix/*`. |
| `feature/<short-name>` | New pages, sections, features | — | Branch from `develop`, PR back into `develop`. Delete after merge. |
| `fix/<short-name>` | Non-urgent bug fixes | — | Same as feature. |
| `content/<short-name>` | New articles, videos, case studies | — | Same as feature. Content is also tested before it goes live. |
| `hotfix/<short-name>` | Urgent fix to production | — | Branch from `main`, PR into `main`, then merge `main` into `develop`. |

## Day-to-day

```bash
# start work
git switch develop && git pull
git switch -c feature/services-pages

# ...commit as you go...
git push -u origin feature/services-pages
# open PR → develop. CI runs; merge → auto-deploys to test

# release: after checking test.ronsystemsai.com
# open PR develop → main. Merge → auto-deploys to prod
git switch main && git pull
git tag -a v1.0.0 -m "Launch" && git push origin v1.0.0
```

## Conventions

- **Commit messages:** `type: short description`, where type is `feat`, `fix`, `content`, `style`, `docs`, `chore`, `refactor`, or `test`.
  Example: `content: add n8n vs Zapier article`
- **Versions:** `vMAJOR.MINOR.PATCH` tags on `main`. `v1.0.0` = public launch.
- **Merge style:** squash-merge feature branches into `develop`; use a merge commit for `develop` → `main` so releases are easy to see.
- **Never commit:** `.env*` files (except `.env.example`), `docs/about-ron/`, secrets, or client data.

## GitHub settings to turn on

- Branch protection on `main` and `develop`: require a PR, require CI to pass, and block force-pushes
- Default branch: `develop` (so PRs target it by default)
- Repository secrets: `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY` (and `GHCR` access via `GITHUB_TOKEN`)
- Consider keeping the repo **private**
