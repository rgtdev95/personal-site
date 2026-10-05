"""Contact-form email through SMTP submission (Proton Mail in production)."""
import logging
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr

from flask import current_app

log = logging.getLogger(__name__)


def send_contact_message(name, email, company, message):
    cfg = current_app.config
    subject = f"Website enquiry from {name}" + (f" ({company})" if company else "")
    body = f"Name: {name}\nEmail: {email}\nBusiness: {company or '-'}\n\n{message}\n"

    if not cfg["SMTP_HOST"]:
        log.warning("SMTP not configured; contact message logged only.\n%s\n%s", subject, body)
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((cfg["SITE_NAME"], cfg["MAIL_FROM"]))
    msg["To"] = cfg["MAIL_TO"]
    msg["Reply-To"] = formataddr((name, email))
    msg.set_content(body)

    try:
        with smtplib.SMTP(cfg["SMTP_HOST"], cfg["SMTP_PORT"], timeout=15) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
            smtp.send_message(msg)
        return True
    except (smtplib.SMTPException, OSError):
        log.exception("Contact message could not be sent")
        return False
