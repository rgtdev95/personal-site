from datetime import date

from flask import Blueprint, Response, current_app, render_template, url_for

from .. import site_content as C
from ..services.content_loader import all_items

bp = Blueprint("seo", __name__)

AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
    "PerplexityBot", "Google-Extended", "Applebot-Extended",
]


def _text(body):
    return Response(body, mimetype="text/plain")


@bp.get("/robots.txt")
def robots():
    site = current_app.config["SITE_URL"]
    if not current_app.config["ALLOW_INDEXING"]:
        return _text("User-agent: *\nDisallow: /\n")
    lines = ["User-agent: *", "Allow: /", "", "# AI assistants and answer engines: allowed on purpose"]
    lines += [f"User-agent: {bot}" for bot in AI_CRAWLERS]
    lines += ["Allow: /", "", f"Sitemap: {site}/sitemap.xml", ""]
    return _text("\n".join(lines))


@bp.get("/sitemap.xml")
def sitemap():
    site = current_app.config["SITE_URL"]
    today = date.today().isoformat()
    urls = [(url_for(e), today) for e in (
        "pages.home", "pages.services", "pages.process", "pages.work",
        "pages.about", "pages.faq", "pages.book", "pages.contact", "pages.privacy",
        "pages.terms",
    )]
    urls += [(url_for("pages.service", slug=s["slug"]), today) for s in C.SERVICES]
    for kind, endpoint in (("resources", "content.resource"), ("videos", "content.video")):
        items = all_items(kind)
        if items:
            urls.append((url_for(f"content.{kind}"), items[0].get("updated") or items[0]["published"]))
        urls += [(url_for(endpoint, slug=i["slug"]), i.get("updated") or i["published"]) for i in items]
    xml = render_template("seo/sitemap.xml", site=site, urls=urls)
    return Response(xml, mimetype="application/xml")


@bp.get("/llms.txt")
def llms():
    body = render_template("seo/llms.txt", C=C, resources=all_items("resources"), videos=all_items("videos"))
    return _text(body)


@bp.get("/.well-known/security.txt")
def security_txt():
    cfg = current_app.config
    year = date.today().year + 1
    return _text(
        f"Contact: mailto:{cfg['CONTACT_EMAIL']}\n"
        f"Expires: {year}-12-31T23:59:59Z\n"
        "Preferred-Languages: en\n"
        f"Canonical: {cfg['SITE_URL']}/.well-known/security.txt\n"
    )


@bp.get("/healthz")
def healthz():
    return _text("ok\n")
