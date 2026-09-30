from os import getenv, path
from dotenv import load_dotenv

from .base import * #noqa
from .base import BASE_DIR




# local environment files
local_env_file = path.join(BASE_DIR, ".envs", ".env.production")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

SITE_NAME = getenv("SITE_NAME")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY",)


ALLOWED_HOSTS = []

ADMINS = [("Api Golden","api.goldenventures@gmail.com"),]
# add changes here
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("SMTP_MAILGUN_PASSWORD")
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO","https")

SECURE_SSL_REDIRECT = getenv("DJANGO_SECURE_SSL_REDIRECT","True") == "True"

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 300

SECURE_HSTS_INCLUDE_SUBDOMANS = (getenv("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS","True") == "True")

SECURE_HSTS_PRELOAD = getenv("DJANGO_SECURE_HSTS_PRELOAD","True") == "True"

SECURE_CONTENT_NOSNIFF = getenv("DJANGO_SECURE_CONTENT_NOSNIFF","True") == "True"

# add trusted domain names(origins) in production
#CSRF_TRUSTED_ORIGINS = ["https://accomm_mngt.com","www.accomm_mngt.com"]

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



