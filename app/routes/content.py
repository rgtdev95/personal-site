from flask import Blueprint, abort, render_template

from .. import site_content as C

from ..services import schema
from ..services.content_loader import all_items, get_item

bp = Blueprint("content", __name__)

KINDS = {
    "resources": {"list": "content.resources", "item": "content.resource", "title": "Guides and articles"},
    "videos": {"list": "content.videos", "item": "content.video", "title": "Videos"},
}


def _list(kind):
    return render_template("content/list.html", C=C, items=all_items(kind), kind=kind, meta=KINDS[kind])


def _item(kind, slug):
    item = get_item(kind, slug)
    if not item:
        abort(404)
    meta = KINDS[kind]
    return render_template(
        "content/item.html",
        C=C,
        item=item,
        kind=kind,
        meta=meta,
        jsonld=[
            schema.article(item, meta["item"]),
            schema.breadcrumbs([(meta["title"], meta["list"], {}), (item["title"], meta["item"], {"slug": slug})]),
        ],
    )


@bp.get("/resources/")
def resources():
    return _list("resources")


@bp.get("/resources/<slug>/")
def resource(slug):
    return _item("resources", slug)


@bp.get("/videos/")
def videos():
    return _list("videos")


@bp.get("/videos/<slug>/")
def video(slug):
    return _item("videos", slug)
