# Production settings
import os
from unipath import Path

PROJECT_ROOT = Path(__file__).ancestor(2)

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    os.environ.get("ADMINS", "Paul Hallett,paulandrewhallett@gmail.com").split(","),
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MANAGERS = ADMINS

BASE_URL = os.environ.get("BASE_URL", "http://pokeapi.co")

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    os.environ.get("ALLOWED_HOSTS", ".pokeapi.co"),
    "localhost",
    "127.0.0.1",
]

TIME_ZONE = os.environ.get("TIME_ZONE", "Europe/London")

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en-gb")

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Explicitly define test runner to avoid warning messages on test execution
TEST_RUNNER = "django.test.runner.DiscoverRunner"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "pokeapi_co_db",
        "USER": "root",
        "PASSWORD": "pokeapi",
        "HOST": "localhost",
        "PORT": "",
        "CONN_MAX_AGE": 30,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "ubx+22!jbo(^x2_scm-o$*py3e@-awu-n^hipkm%2l$sw$&2l#"
)

CUSTOM_APPS = ("pokemon_v2",)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.messages",
    "django.contrib.humanize",
    "corsheaders",
    "rest_framework",
    "cachalot",
    "drf_spectacular",
) + CUSTOM_APPS


API_LIMIT_PER_PAGE = 1

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

CORS_URLS_REGEX = r"^/api/.*$"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
    "PAGINATE_BY": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # For teaching purposes - allow anonymous writes (in production, add proper authentication)
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SPECTACULAR_SETTINGS = {
    "TITLE": "PokéAPI",
    "DESCRIPTION": """All the Pokémon data you'll ever need in one place, easily accessible through a modern free open-source RESTful API.

## What is this?

This is a full RESTful API linked to an extensive database detailing everything about the Pokémon main game series.

We've covered everything from Pokémon to Berry Flavors.

## Where do I start?

We have awesome [documentation](https://pokeapi.co/docs/v2) on how to use this API. It takes minutes to get started.

This API will always be publicly available and will never require any extensive setup process to consume.

Created by [**Paul Hallett**](https://github.com/phalt) and other [**PokéAPI contributors***](https://github.com/PokeAPI/pokeapi#contributing) around the world. Pokémon and Pokémon character names are trademarks of Nintendo.
    """,
    "SORT_OPERATIONS": False,
    "SERVERS": [{"url": "https://pokeapi.co"}],
    "EXTERNAL_DOCS": {"url": "https://pokeapi.co/docs/v2"},
    "VERSION": "2.7.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "OAS_VERSION": "3.1.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "TAGS": [
        {
            "name": "pokemon",
            "description": "Pokémon are the creatures that inhabit the world of the Pokémon games. They can be caught using Pokéballs and trained by battling with other Pokémon. Each Pokémon belongs to a specific species but may take on a variant which makes it differ from other Pokémon of the same species, such as base stats, available abilities and typings. See [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_(species)) for greater detail.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon",
            },
        },
        {
            "name": "evolution",
            "description": "Evolution is a process in which a Pokémon changes into a different species of Pokémon.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/Evolution",
            },
        },
        {
            "name": "berries",
            "description": "Berries can be soft or hard. Check out [Bulbapedia](http://bulbapedia.bulbagarden.net/wiki/Category:Berries_by_firmness) for greater detail.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/Berry",
            },
        },
        {
            "name": "items",
            "description": "An item is an object in the games which the player can pick up, keep in their bag, and use in some manner. They have various uses, including healing, powering up, helping catch Pokémon, or to access a new area.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/Item",
            },
        },
        {
            "name": "machines",
            "description": "Machines are the representation of items that teach moves to Pokémon. They vary from version to version, so it is not certain that one specific TM or HM corresponds to a single Machine.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/TM",
            },
        },
        {
            "name": "location",
            "description": "Locations that can be visited within the games. Locations make up sizable portions of regions, like cities or routes.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/List_of_locations_by_index_number",
            },
        },
        {
            "name": "contest",
            "description": "Pokémon Contests are a type of competition often contrasted with Pokémon battles and held in Contest Halls",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Contest",
            },
        },
        {
            "name": "moves",
            "description": "Moves are the skills of Pokémon in battle. In battle, a Pokémon uses one move each turn. Some moves (including those learned by Hidden Machine) can be used outside of battle as well, usually for the purpose of removing obstacles or exploring new areas.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/List_of_locations_by_name",
            },
        },
        {"name": "encounters"},
        {
            "name": "games",
            "description": "The Pokémon games are all video games in the Pokémon franchise.",
            "externalDocs": {
                "description": "Find more info here",
                "url": "https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_games",
            },
        },
        {"name": "utility"},
    ],
}

# Railway Production Configuration
RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT')

if RAILWAY_ENVIRONMENT:
    import dj_database_url
    print("🚂 Running on Railway - using production settings")

    # Production settings override
    DEBUG = False

    # Railway provides these automatically
    ALLOWED_HOSTS = [
        '.railway.app',
        '.up.railway.app',
        'localhost',
        '127.0.0.1'
    ]

    # Database configuration for Railway PostgreSQL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
        # Optimize database connections for Railway's memory limits
        DATABASES['default']['CONN_MAX_AGE'] = 60
        DATABASES['default']['OPTIONS'] = {
            'MAX_CONNS': 20,
            'OPTIONS': {
                'MAX_CONNS': 1
            }
        }
        print(f"✅ Connected to Railway PostgreSQL database")

    # Memory optimizations for Railway
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'OPTIONS': {
                'MAX_ENTRIES': 1000,  # Limit cache size
                'CULL_FREQUENCY': 3,
            }
        }
    }

    # Static files with WhiteNoise (add to beginning of middleware)
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
        MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + list(MIDDLEWARE)

    # Static files configuration
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Update CORS for Railway domains
    CORS_ALLOWED_ORIGINS = [
        "https://*.railway.app",
        "https://*.up.railway.app",
    ]
    CORS_ALLOW_ALL_ORIGINS = True  # For educational purposes

    # Security settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = False  # Railway handles this

    # Memory optimizations for Railway's 1GB limit
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Disable admin in production to save memory
    INSTALLED_APPS = tuple(app for app in INSTALLED_APPS if app != 'django.contrib.admin')

    # Optimize logging to reduce memory usage
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
    }

    # Disable migrations logging to save memory
    MIGRATION_MODULES = {}

    print("🎓 Educational PokéAPI optimized for Railway deployment!")

