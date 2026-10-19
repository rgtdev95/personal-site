from flask import Blueprint, abort, current_app, flash, redirect, render_template, url_for

from .. import limiter
from .. import site_content as C
from ..forms import ContactForm
from ..services import schema
from ..services.mailer import send_contact_message

bp = Blueprint("pages", __name__)


@bp.get("/")
def home():
    return render_template(
        "pages/home.html",
        C=C,
        jsonld=[schema.organization(), schema.person(), schema.website(), schema.faq(C.FAQS)],
    )


@bp.get("/services/")
def services():
    return render_template(
        "pages/services.html",
        C=C,
        jsonld=[schema.organization(), schema.breadcrumbs([("Services", "pages.services", {})])],
    )


@bp.get("/services/<slug>/")
def service(slug):
    item = C.service_by_slug(slug)
    if not item:
        abort(404)
    others = [s for s in C.SERVICES if s["slug"] != slug]
    return render_template(
        "pages/service.html",
        C=C,
        s=item,
        others=others,
        jsonld=[
            schema.service(item),
            schema.faq(item["faqs"]),
            schema.breadcrumbs([("Services", "pages.services", {}), (item["name"], "pages.service", {"slug": slug})]),
        ],
    )


@bp.get("/process/")
def process():
    return render_template(
        "pages/process.html",
        C=C,
        jsonld=[schema.organization(), schema.breadcrumbs([("How it works", "pages.process", {})])],
    )


@bp.get("/work/")
def work():
    return render_template(
        "pages/work.html",
        C=C,
        jsonld=[schema.organization(), schema.breadcrumbs([("Work", "pages.work", {})])],
    )


@bp.get("/about/")
def about():
    return render_template(
        "pages/about.html",
        C=C,
        jsonld=[schema.person(), schema.breadcrumbs([("About", "pages.about", {})])],
    )


@bp.get("/faq/")
def faq():
    return render_template(
        "pages/faq.html",
        C=C,
        jsonld=[schema.faq(C.FAQS), schema.breadcrumbs([("FAQ", "pages.faq", {})])],
    )


@bp.get("/book/")
def book():
    return render_template(
        "pages/book.html",
        C=C,
        form=ContactForm(),
        jsonld=[schema.breadcrumbs([("Book a call", "pages.book", {})])],
    )


@bp.route("/contact/", methods=["GET", "POST"])
@limiter.limit("5 per hour", methods=["POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if form.website.data:  # honeypot: bots fill every field
            return redirect(url_for("pages.contact_sent"))
        ok = send_contact_message(
            name=form.name.data,
            email=form.email.data,
            company=form.company.data,
            message=form.message.data,
        )
        if ok:
            return redirect(url_for("pages.contact_sent"))
        flash(
            f"Your message couldn't be sent just now. Please try again, or email {current_app.config['CONTACT_EMAIL']} directly.",
            "error",
        )
    return render_template(
        "pages/contact.html",
        C=C,
        form=form,
        jsonld=[schema.breadcrumbs([("Contact", "pages.contact", {})])],
    ), (422 if form.errors else 200)


@bp.get("/contact/sent/")
def contact_sent():
    return render_template("pages/contact_sent.html")


@bp.get("/privacy/")
def privacy():
    return render_template("pages/privacy.html")


@bp.get("/terms/")
def terms():
    return render_template("pages/terms.html")
