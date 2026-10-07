from os import getenv, path
from dotenv import load_dotenv

from .base import *  # noqa
from .base import BASE_DIR

# Production environment file (used for local testing of prod settings)
env_file = path.join(BASE_DIR, ".envs", ".env.production")
if path.isfile(env_file):
    load_dotenv(env_file)

SITE_NAME = getenv("SITE_NAME")

SECRET_KEY = getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

ADMINS = [("Api Golden", "api.goldenventures@gmail.com")]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("SMTP_MAILGUN_PASSWORD")
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = getenv("DJANGO_SECURE_SSL_REDIRECT", "True") == "True"

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = int(getenv("DJANGO_SECURE_HSTS_SECONDS", "2592000"))

SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    getenv("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
)

SECURE_HSTS_PRELOAD = getenv("DJANGO_SECURE_HSTS_PRELOAD", "True") == "True"

SECURE_CONTENT_NOSNIFF = (
    getenv("DJANGO_SECURE_CONTENT_NOSNIFF", "True") == "True"
)

CSRF_TRUSTED_ORIGINS = getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"




LOGGING = {
    "version":1,
    "disable_existing_loggers":False,
    "filters":{"require_debug_false":{"()":"django.utils.log.RequireDebugFalse"}},
    "formatters":{
        "verbose":{
            "format":"%(levelname)s %(name)s-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s "
        }
    },
    "handlers":{
        "mail_admins":{
            "level":"ERROR",
            "filters":["require_debug_false"],
            "class":"django.utils.log.AdminEmailHandler"
        },
        "console":{
            "level":"DEBUG",
            "class":"logging.StreamHandler", 
            "formatter":"verbose"
            }
    },
    "root":{"level":"INFO","handlers":["console"]},
    "loggers":{
        "django.request":{
            "handlers":["mail_admins"],
            "level":"ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost":{
            "handlers":["console","mail_admins"],
            "level":"ERROR",
            "propagate": True,
        }
    }
}



