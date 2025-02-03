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


