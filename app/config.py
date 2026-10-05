"""Configuration, selected by the APP_ENV environment variable."""
import os


def _env(name, default=""):
    return os.environ.get(name, default).strip()


class BaseConfig:
    APP_ENV = "development"
    SECRET_KEY = _env("SECRET_KEY", "dev-only-not-secret")
    SITE_URL = _env("SITE_URL", "http://127.0.0.1:5000").rstrip("/")
    SITE_NAME = "Ron Systems AI"

    # Search engines and AI crawlers may index this environment.
    ALLOW_INDEXING = False

    CONTACT_EMAIL = _env("CONTACT_EMAIL", "hello@ronsystemsai.com")
    CALENDLY_URL = _env("CALENDLY_URL")  # empty = booking falls back to the contact form

    # Social profiles render only when set.
    SOCIAL = {
        "YouTube": _env("SOCIAL_YOUTUBE"),
        "Facebook": _env("SOCIAL_FACEBOOK"),
        "LinkedIn": _env("SOCIAL_LINKEDIN"),
        "GitHub": _env("SOCIAL_GITHUB"),
    }

    # Umami analytics renders only when both are set.
    UMAMI_SCRIPT_URL = _env("UMAMI_SCRIPT_URL")
    UMAMI_WEBSITE_ID = _env("UMAMI_WEBSITE_ID")

    # Contact-form mail (Proton SMTP submission). Empty host = log only.
    SMTP_HOST = _env("SMTP_HOST")
    SMTP_PORT = int(_env("SMTP_PORT", "587"))
    SMTP_USER = _env("SMTP_USER")
    SMTP_PASSWORD = _env("SMTP_PASSWORD")
    MAIL_FROM = _env("MAIL_FROM", "hello@ronsystemsai.com")
    MAIL_TO = _env("MAIL_TO", "hello@ronsystemsai.com")

    CONTENT_DIR = _env("CONTENT_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "content"))

    RATELIMIT_STORAGE_URI = "memory://"
    WTF_CSRF_TIME_LIMIT = 60 * 60 * 4
    # The only cookie: Flask's session, holding the contact form's CSRF token until the browser closes.
    SESSION_COOKIE_SAMESITE = "Lax"
    SEND_FILE_MAX_AGE_DEFAULT = 60 * 60 * 24 * 365  # static URLs are cache-busted by file hash


class DevelopmentConfig(BaseConfig):
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestConfig(BaseConfig):
    APP_ENV = "test"
    SESSION_COOKIE_SECURE = True


class ProductionConfig(BaseConfig):
    APP_ENV = "production"
    ALLOW_INDEXING = True
    SESSION_COOKIE_SECURE = True


class TestingConfig(BaseConfig):
    """Used by pytest."""
    APP_ENV = "testing"
    TESTING = True
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False


CONFIGS = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
