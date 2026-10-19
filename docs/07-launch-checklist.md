# 07 — Launch checklist (including things easy to miss)

## Identity and trust

- [ ] **Register `ronsystemsai.com`** (confirm at the registrar) and claim `@ronsystemsai` on Facebook, YouTube, and LinkedIn
- [ ] **Proton Mail on the domain** (`hello@ronsystemsai.com`), replacing the Gmail address on the site. Add Proton's DNS records (verification, MX, SPF, DKIM, DMARC) and create an SMTP token for the contact form (check your plan includes SMTP submission)
- [ ] Professional photo on the site (the current design has a `showPhoto` option but no photo yet)
- [ ] Real **Calendly** link (the current design points to the placeholder `https://calendly.com/`)
- [ ] LinkedIn headline and about section rewritten from job-seeker to consultant
- [x] `docs/about-ron/` (resume with phone number) is in `.gitignore`

## Proof

- [ ] 3–5 anonymized case studies written up in problem → what I built → result form
- [ ] Ask current and past clients for a short testimonial (with permission to publish name, role, and country)
- [ ] Start measuring results on every project (hours saved per week, errors reduced, response time) so later case studies have real numbers
- [ ] Certifications worth listing, if any (AWS, Microsoft, n8n, etc.)

## Business and legal (for working with overseas clients)

- [ ] **Business registration and tax** in the Philippines as a freelancer or sole proprietor (DTI + BIR). Check with an accountant
- [ ] **Getting paid internationally:** Wise, Payoneer, Stripe, or PayPal. Invoice in USD and/or the client's currency
- [ ] **Contract templates:** a services agreement plus a statement of work (scope, deliverables, change requests, payment terms, IP ownership, and liability limit)
- [ ] **Confidentiality / NDA** template
- [ ] **Data Processing Agreement (DPA)**: EU/UK clients will need one because you'll handle their data (GDPR). Australian clients expect Privacy Act awareness
- [ ] Access and credentials handling policy (how you store and return client passwords and keys, e.g. a shared Vaultwarden/Bitwarden vault they own)
- [ ] Consider **professional indemnity insurance** once projects grow

## Website legal pages

- [ ] Privacy policy (GDPR-, UK GDPR-, AU Privacy Act-, and CCPA-aware; cover what the contact form, analytics, and Calendly collect)
- [ ] Terms of service: plain-English draft at `/terms/` (website use only; client work runs on the signed agreement). Confirm the governing law and have a lawyer review before launch
- [ ] No cookie banner needed: Umami is cookie-less, and the only cookie is the strictly necessary `session` cookie holding the contact form's CSRF token (disclosed on `/privacy/`; `Secure` + `SameSite=Lax` in test and production). Recheck if any cookie-setting script is added later (the Calendly embed sets its own cookies only on the booking page, so mention it in the privacy policy)
- [ ] Accessibility statement (optional; WCAG 2.2 AA target)

## Lead handling

- [ ] Contact form that sends to your domain email, with spam protection
- [ ] Auto-reply + intake questions before the call (Calendly questions: company size, tools used, main problem)
- [ ] Simple CRM or pipeline for leads. Run it on your own automation, which also makes good content
- [ ] Optional **lead magnet**: e.g. "The small-business automation checklist" PDF in exchange for an email

## Technical launch

- [ ] Everything in [05-search-and-ai-visibility.md](05-search-and-ai-visibility.md) section 1
- [ ] Security headers (CSP, HSTS). Your security background makes it worth getting an A on securityheaders.com
- [ ] `/.well-known/security.txt` (a small touch that fits a security-minded consultant)
- [ ] Uptime monitoring on the site itself
- [ ] Backups: git remote for source; off-server backups of the VPS `.env` files
- [ ] Test site blocked from indexing and behind basic auth (see [09-architecture-and-deployment.md](09-architecture-and-deployment.md))
