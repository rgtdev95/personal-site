"""Markdown content with YAML front-matter: content/<kind>/<slug>.md

Required front-matter: title, description, published (YYYY-MM-DD).
Optional: updated, draft (true hides it), youtube_id (videos).
"""
import os
from datetime import date
from functools import lru_cache

import markdown
import yaml
from flask import current_app

REQUIRED = ("title", "description", "published")


def _parse(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    if not raw.startswith("---"):
        raise ValueError(f"{path}: missing front-matter")
    _, fm, body = raw.split("---", 2)
    meta = yaml.safe_load(fm) or {}
    missing = [k for k in REQUIRED if k not in meta]
    if missing:
        raise ValueError(f"{path}: missing {', '.join(missing)}")
    for key in ("published", "updated"):
        if isinstance(meta.get(key), date):
            meta[key] = meta[key].isoformat()
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["html"] = markdown.markdown(body, extensions=["extra", "sane_lists", "toc"])
    return meta


@lru_cache(maxsize=8)
def _load(content_dir, kind, _debug_bust):
    folder = os.path.join(content_dir, kind)
    if not os.path.isdir(folder):
        return ()
    items = [
        _parse(os.path.join(folder, name))
        for name in sorted(os.listdir(folder))
        if name.endswith(".md") and not name.startswith("_")
    ]
    items = [i for i in items if not i.get("draft")]
    return tuple(sorted(items, key=lambda i: i["published"], reverse=True))


def all_items(kind):
    cfg = current_app.config
    bust = os.urandom(4) if current_app.debug else None
    return list(_load(cfg["CONTENT_DIR"], kind, bust))


def get_item(kind, slug):
    return next((i for i in all_items(kind) if i["slug"] == slug), None)
