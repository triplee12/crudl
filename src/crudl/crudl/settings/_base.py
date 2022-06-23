from pathlib import Path
import os
import json
import sys
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from crudl.apps.utils.versioning import get_git_changeset_timestamp

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


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.forms",
    # third party app
    "django_json_ld",
    "crispy_forms",
    "qr_code",
    "haystack",
    "django_elasticsearch_dsl",
    "sekizai",
    "ordered_model",
    'crudl.apps.accounts.apps.SocialDjangoConfig',
    "imagekit",
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
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                "crudl.apps.core.context_processors.website_url",
                "sekizai.context_processors.sekizai",
                "crudl.apps.core.context_processors.google_maps",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Crispy-form
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

WSGI_APPLICATION = 'crudl.wsgi.application'


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

# GOOGLE API CONFIGURATIONS
GOOGLE_MAPS_API_KEY = get_secret("GOOGLE_MAPS_API_KEY")

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ("bg", "Bulgarian"), ("hr", "Croatian"),
    ("cs", "Czech"), ("da", "Danish"),
    ("nl", "Dutch"), ("en", "English"),
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
HAYSTACK_CONNECTIONS = {}
for lang_code, lang_name in LANGUAGES:
    lang_code_underscored = lang_code.replace("-", "_")
    HAYSTACK_CONNECTIONS[f"default_{lang_code_underscored}"] = {
        "ENGINE":"crudl.apps.search.multilingual_whoosh_backend.MultilingualWhooshEngine",
        "PATH": os.path.join(BASE_DIR, "tmp", f"whoosh_index_{lang_code_underscored}"),
    }
    lang_code_underscored = LANGUAGE_CODE.replace("-", "_")
    HAYSTACK_CONNECTIONS["default"] = HAYSTACK_CONNECTIONS[
        f"default_{lang_code_underscored}"
    ]

# Elasticsearch Dsl
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}