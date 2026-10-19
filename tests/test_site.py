import json
import re

import pytest

from app import create_app
from app import site_content as C


@pytest.fixture
def app():
    return create_app("testing")


@pytest.fixture
def client(app):
    return app.test_client()


PAGES = ["/", "/services/", "/process/", "/work/", "/about/", "/faq/", "/book/", "/contact/", "/privacy/", "/terms/", "/resources/", "/videos/"]


@pytest.mark.parametrize("path", PAGES + [f"/services/{s['slug']}/" for s in C.SERVICES])
def test_pages_render(client, path):
    resp = client.get(path)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert html.count("<h1") == 1, "exactly one h1 per page"
    assert '<link rel="canonical"' in html
    assert "style=" not in html, "inline styles are blocked by the CSP"


def test_404(client):
    resp = client.get("/nope/")
    assert resp.status_code == 404
    assert "isn't on the rail" in resp.get_data(as_text=True)


def test_jsonld_is_valid_json(client):
    html = client.get("/").get_data(as_text=True)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert blocks
    types = {json.loads(b)["@type"] for b in blocks}
    assert {"ProfessionalService", "Person", "WebSite", "FAQPage"} <= types


def test_no_prices_or_timezone_claims(client):
    for path in PAGES:
        text = client.get(path).get_data(as_text=True)
        assert not re.search(r"[$€£]\s?\d", text), f"price figure on {path}"
        assert "UTC" not in text and "time zone" not in text.replace("your own time zone", ""), f"time-zone claim on {path}"
        assert "Working with clients in" not in text


def test_robots_blocks_non_production(client):
    body = client.get("/robots.txt").get_data(as_text=True)
    assert "Disallow: /" in body


def test_robots_allows_ai_crawlers_in_production():
    client = create_app("production").test_client()
    body = client.get("/robots.txt").get_data(as_text=True)
    assert "GPTBot" in body and "ClaudeBot" in body and "Disallow" not in body
    assert "X-Robots-Tag" not in client.get("/").headers


def test_test_env_sends_noindex_header():
    client = create_app("test").test_client()
    assert client.get("/").headers["X-Robots-Tag"] == "noindex, nofollow"


def test_security_headers(client):
    csp = client.get("/").headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp and "frame-ancestors 'none'" in csp


def test_sitemap_lists_services(client):
    xml = client.get("/sitemap.xml").get_data(as_text=True)
    for s in C.SERVICES:
        assert f"/services/{s['slug']}/" in xml
    assert "/terms/" in xml


@pytest.mark.parametrize("env", ["production", "test"])
def test_session_cookie_is_secure_and_same_site(env):
    # The contact form's CSRF token is the site's only cookie; the privacy page describes it.
    cookie = create_app(env).test_client().get("/contact/").headers["Set-Cookie"]
    assert cookie.startswith("session=")
    assert "Secure" in cookie and "SameSite=Lax" in cookie and "HttpOnly" in cookie
    assert "Expires" not in cookie, "a browser-session cookie, as the privacy page says"


def test_footer_shows_every_social_logo_but_links_only_set_urls(app):
    app.config["SOCIAL"] = {"YouTube": "", "Facebook": "", "LinkedIn": "https://example.com/in", "GitHub": ""}
    html = app.test_client().get("/").get_data(as_text=True)
    for name in ("youtube", "facebook", "linkedin", "github"):
        assert f'href="#i-{name}"' in html
    assert html.count('<a class="social__link"') == 1
    assert 'href="https://example.com/in"' in html
    assert html.count("social__link--off") == 3


def test_home_sets_no_cookies(client):
    assert "Set-Cookie" not in client.get("/").headers


def test_llms_txt(client):
    body = client.get("/llms.txt").get_data(as_text=True)
    assert body.startswith("# Ron Systems AI")


def test_healthz(client):
    assert client.get("/healthz").status_code == 200


def test_contact_form_validation(client):
    resp = client.post("/contact/", data={"name": "", "email": "bad", "message": "hi"})
    assert resp.status_code == 422
    html = resp.get_data(as_text=True)
    assert "Please tell me your name." in html
    assert "look right" in html


def test_contact_form_success_logs_without_smtp(client):
    resp = client.post("/contact/", data={"name": "Sam", "email": "sam@example.com", "message": "We re-type every invoice."})
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/contact/sent/")


def test_honeypot_silently_drops(client, monkeypatch):
    sent = []
    monkeypatch.setattr("app.routes.pages.send_contact_message", lambda **kw: sent.append(kw) or True)
    resp = client.post("/contact/", data={"name": "Bot", "email": "b@example.com", "message": "Buy now buy now", "website": "x"})
    assert resp.status_code == 302 and not sent
