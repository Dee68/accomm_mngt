from os import getenv, path
from dotenv import load_dotenv

from .base import * #noqa
from .base import BASE_DIR




# local environment files
local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

SITE_NAME = getenv("SITE_NAME")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY","1mXdITfSBRkJuodNHdvYniIjDCCsYNWq-VX3fwDo4dp7t0R8uGs")

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

DEBUG = True

ALLOWED_HOSTS = ["localhost","127.0.0.1","0.0.0.0"]

ADMIN_URL = getenv("DJANGO_ADMIN_URL")
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

LOGGING = {
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "verbose":{
            "format":"%(levelname)s %(name)s-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s "
        }
    },
    "handlers":{
        "console":{
            "level":"DEBUG",
            "class":"logging.StreamHandler", 
            "formatter":"verbose"
            }
    },
    "root":{"level":"INFO","handlers":["console"]}
}
