from .base import *

ALLOWED_HOSTS = ["35.72.146.206", "pybobbs.ga"]
STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = []
DEBUG = False
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "pybo",
        "USER": "dbmasteruser",
        "PASSWORD": "uyh>Y>$Vjgqwb#T8]OM5gh5XHQ%an9H!",
        "HOST": "ls-2c9541fba25656f1fc14a134908ed69936494f00.chyzn53nkdwf.ap-northeast-1.rds.amazonaws.com",
        "PORT": "5432",
    }
}
