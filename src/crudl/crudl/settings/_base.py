from pathlib import Path
import os
import json
import sys
from telnetlib import AUTHENTICATION
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from crudl.apps.utils.versioning import get_git_changeset_timestamp
from crudl.apps.auth_extra.password_validation import (
    SpecialCharacterInclusionValidator,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Get secret config
with open(os.path.join(os.path.dirname(__file__), 'secrets.json'), 'r') as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    """Get secret environment variables or return explicit exception"""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

WSGI_APPLICATION = 'crudl.wsgi.application'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.forms",
    "django.contrib.sitemaps",
    # third party app
    "rest_framework",
    #"admin_honeypot",
    "crudl.apps.admin_honeypot_fix.apps.AdminHoneypotFixConfig",
    "django_json_ld",
    "crispy_forms",
    "qr_code",
    "haystack",
    "django_elasticsearch_dsl",
    "sekizai",
    "ordered_model",
    'crudl.apps.accounts.apps.SocialDjangoConfig',
    "imagekit",
    # "social_django",
    "mptt",
    "django_mptt_admin",
    "treebeard",
    # Own apps
    "crudl.apps.accounts",
    "crudl.apps.core",
    "crudl.apps.category",
    "crudl.apps.ideas",
    'crudl.apps.magazine',
    "crudl.apps.search",
    "crudl.apps.locations",
    "crudl.apps.likes",
    "crudl.apps.products",
    "crudl.apps.music",
    "crudl.apps.news",
    "crudl.apps.viral_videos",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #"csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = 'crudl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'crudl', 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "sekizai.context_processors.sekizai",
                "crudl.apps.core.context_processors.website_url",
                "crudl.apps.core.context_processors.google_maps",
                "crudl.apps.external_auth.context_processors.auth0",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = {
    "crudl.apps.external_auth.backends.Auth0",
    "django.contrib.auth.backends.ModelBackend",
}

LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/dashboard"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Crispy-form
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        'NAME': get_secret('DATABASE_NAME'),
        'USER': get_secret('DATABASE_USER'),
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Memcached Config
# CACHES = {
#     "memcached": {
#         "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
#         "LOCATION": get_secret("CACHE_LOCATION"),
#         "TIMEOUT": 60, # 1 minute timeout
#         "KEY_PREFIX": "crudl",
#     },
# }
# CACHES["default"] = CACHES["memcached"]

# REDIS CACHES
CACHES = {
    "redis": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": get_secret("CACHE_LOCATION"),
        "TIMEOUT": 60, # 1 minute timeout
        "KEY_PREFIX": "crudl",
    },
}
CACHES["default"] = CACHES["redis"]

# REST_FRAMEWORK CONFIGURATIONS
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [ "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
}

# GOOGLE API CONFIGURATIONS
GOOGLE_MAPS_API_KEY = get_secret("GOOGLE_MAPS_API_KEY")

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        "OPTIONS": {"max_similarity": 0.7},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        "OPTIONS": {"min_length": 12},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        "NAME": "crudl.apps.auth_extra.password_validation.MaximumLengthValidator",
        "OPTIONS": {"max_length": 32},
    },
    {
        "NAME": "crudl.apps.auth_extra.password_validation.SpecialCharacterInclusionValidator",
        "OPTIONS": {"special_chars": ("{", "}", "^", "&") + SpecialCharacterInclusionValidator.DEFAULT_SPECIAL_CHARACTERS},
    },
]
AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ("bg", "Bulgarian"),
    ("hr", "Croatian"),
    ("cs", "Czech"),
    ("da", "Danish"),
    ("nl", "Dutch"),
    ("en", "English"),
    ("et", "Estonian"),
    ("fi", "Finnish"),
    ("fr", "French"),
    ("de", "German"),
    ("el", "Greek"),
    ("hu", "Hungarian"),
    ("ga", "Irish"), 
    ("it", "Italian"),
    ("lv", "Latvian"),
    ("lt", "Lithuanian"),
    ("mt", "Maltese"),
    ("pl", "Polish"),
    ("pt", "Portuguese"),
    ("ro", "Romanian"),
    ("sk", "Slovak"), 
    ("sl", "Slovene"),
    ("es", "Spanish"), 
    ("sv", "Swedish"),
]

LANGUAGES_EXCEPT_THE_DEFAULT = [
    ("bg", "Bulgarian"), ("hr", "Croatian"),
    ("cs", "Czech"), ("da", "Danish"),
    ("nl", "Dutch"),
    ("et", "Estonian"), ("fi", "Finnish"),
    ("fr", "French"), ("de", "German"),
    ("el", "Greek"), ("hu", "Hungarian"),
    ("ga", "Irish"), ("it", "Italian"),
    ("lv", "Latvian"), ("lt", "Lithuanian"),
    ("mt", "Maltese"), ("pl", "Polish"),
    ("pt", "Portuguese"), ("ro", "Romanian"),
    ("sk", "Slovak"), ("sl", "Slovene"),
    ("es", "Spanish"), ("sv", "Swedish"),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

with open(os.path.join(BASE_DIR, 'crudl', 'settings', 'last-modified.txt'), 'r') as f:
    timestamp = f.readline().strip()
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
timestamp = get_git_changeset_timestamp(BASE_DIR)
STATIC_URL = f'/static/' # Add {timestamp} to static and media url if you want to get the latest git change timestamp
MEDIA_URL = f'/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'crudl', 'crudl_static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Social Auth
SOCIAL_AUTH_JSONFIELD_ENABLED = True

# External modules
EXTERNAL_BASE = os.path.join(BASE_DIR, 'externals')
EXTERNAL_LIBS_PATH = os.path.join(EXTERNAL_BASE, 'libs')
EXTERNAL_APPS_PATH = os.path.join(EXTERNAL_BASE, 'apps')
sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path

# Magazine NewsArticle Choices

MAGAZINE_ARTICLE_THEME_CHOICES = [
    ('futurism', _("Futurism")),
    ('nostalgia', _("Nostalgia")),
    ('sustainability', _("Sustainability")),
    ('wonder', _("Wonder")),
    ('positivity', _("Positivity")),
    ('solutions', _("Solutions")),
    ('science', _("Science")),
]

# Haystack Settings
# HAYSTACK_CONNECTIONS = {}
# for lang_code, lang_name in LANGUAGES:
#     lang_code_underscored = lang_code.replace("-", "_")
#     HAYSTACK_CONNECTIONS[f"default_{lang_code_underscored}"] = {
#         "ENGINE": "crudl.apps.search.multilingual_whoosh_backend.MultilingualWhooshEngine",
#         "PATH": os.path.join(BASE_DIR, "tmp", f"whoosh_index_{lang_code_underscored}"),
#     }
#     lang_code_underscored = LANGUAGE_CODE.replace("-", "_")
#     HAYSTACK_CONNECTIONS["default"] = HAYSTACK_CONNECTIONS[
#         f"default_{lang_code_underscored}"
#     ]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    }
}

# Elasticsearch Dsl
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}

# CSP Config
CSP_DEFAULT_SRC = [
    "'self'",
    "https://stackpath.bootstrapcdn.com/",
]
CSP_SCRIPT_SRC = [
    "'self'",
    "https://stackpath.bootstrapcdn.com/",
    "https://code.jquery.com/",
    "https://cdnjs.cloudflare.com/",
]
CSP_IMG_SRC = ["*", "data:"]
CSP_FRAME_SRC = ["*"]

# Social Config
SOCIAL_AUTH_AUTH0_DOMAIN = get_secret("AUTH0_DOMAIN")
SOCIAL_AUTH_AUTH0_KEY = get_secret("AUTH0_KEY")
SOCIAL_AUTH_AUTH0_SECRET = get_secret("AUTH0_SECRET")
SOCIAL_AUTH_AUTH0_SCOPE = get_secret("AUTH0_SCOPE")
SOCIAL_AUTH_TRAILING_SLASH = False
# API KEYS
LAST_FM_API_KEY = get_secret("LAST_FM_API_KEY")

# Logging configuration
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "tmp", "debug.log"),
#         }
#     },
#     "loggers": {"django": {"handlers": ["file"], "level": "DEBUG", "propagate": True}},
# }
