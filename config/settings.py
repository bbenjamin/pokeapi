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

# Database Configuration
# Check for Railway DATABASE_URL first, then fallback to local
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Railway PostgreSQL configuration
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL)
    }
    print(f"🚂 Using Railway PostgreSQL database")
else:
    # Local development database
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
    print(f"💻 Using local PostgreSQL database")

# Cache Configuration - Railway compatible (no Redis dependency)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default-cache",
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
            "CULL_FREQUENCY": 3,
        }
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

# Determine the correct server URL based on environment
if DATABASE_URL and 'railway' in DATABASE_URL:
    # Railway production environment
    API_SERVER_URL = "https://pokeapi-production-2219.up.railway.app"
    DOCS_URL = "https://pokeapi-production-2219.up.railway.app/api/v2/schema/swagger-ui/"
else:
    # Local development or original
    API_SERVER_URL = "http://localhost:8000" if DEBUG else "https://pokeapi.co"
    DOCS_URL = "https://pokeapi.co/docs/v2"

SPECTACULAR_SETTINGS = {
    "TITLE": "🎓 Educational PokéAPI - Writable REST API",
    "DESCRIPTION": """**Educational version of PokéAPI with full CRUD operations for learning REST API concepts**

## What is this?

This is an enhanced version of the popular PokéAPI that includes **writable endpoints** for teaching REST API concepts. Students can practice all HTTP methods (GET, POST, PUT, PATCH, DELETE) with interactive Pokemon data.

## Educational Features

- 🔄 **Full CRUD Operations** - Create, Read, Update, Delete Pokemon data
- 📚 **Interactive Documentation** - Hands-on API testing with Swagger UI
- 🎯 **Teaching-Focused** - Sample data perfect for learning REST concepts  
- 🌐 **CORS Enabled** - Ready for frontend development exercises

## Educational Endpoints

- `/api/v2/writable-pokemon/` - Practice Pokemon CRUD operations
- `/api/v2/writable-ability/` - Learn with Pokemon abilities  
- `/api/v2/writable-type/` - Explore Pokemon type system
- `/api/v2/writable-berry/` - Work with Pokemon berries

## Original PokéAPI

Based on the amazing [PokéAPI](https://pokeapi.co) created by [**Paul Hallett**](https://github.com/phalt) and [**contributors**](https://github.com/PokeAPI/pokeapi#contributing). Pokémon and Pokémon character names are trademarks of Nintendo.
    """,
    "SORT_OPERATIONS": False,
    "SERVERS": [{"url": API_SERVER_URL, "description": "Educational PokéAPI Server"}],
    "EXTERNAL_DOCS": {"url": DOCS_URL, "description": "API Documentation"},
    "VERSION": "2.7.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "OAS_VERSION": "3.1.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "TAGS": [
        {
            "name": "pokemon-writable",
            "description": "🎓 **Educational CRUD Operations** - Create, read, update, and delete Pokemon for hands-on REST API learning. Practice all HTTP methods with interactive Pokemon data.",
            "externalDocs": {
                "description": "Learn REST API concepts",
                "url": "https://restfulapi.net/",
            },
        },
        {
            "name": "berries-writable",
            "description": "🫐 **Educational Berry Management** - Practice CRUD operations with Pokemon berries. Perfect for learning REST API patterns and JSON handling.",
        },
        {
            "name": "abilities-writable",
            "description": "💪 **Educational Ability System** - Learn API design by managing Pokemon abilities. Full create, read, update, delete functionality for educational purposes.",
        },
        {
            "name": "types-writable",
            "description": "🏷️ **Educational Type System** - Explore REST concepts through Pokemon type management. Complete CRUD operations available for learning.",
        },
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
PORT = os.environ.get('PORT')  # Railway sets PORT environment variable

print(f"🔍 Environment check:")
print(f"   DATABASE_URL exists: {bool(DATABASE_URL)}")
print(f"   RAILWAY_ENVIRONMENT: {RAILWAY_ENVIRONMENT}")
print(f"   PORT: {PORT}")

# Detect Railway by RAILWAY_ENVIRONMENT or PORT (Railway always sets PORT)
IS_RAILWAY = RAILWAY_ENVIRONMENT or PORT

if IS_RAILWAY:
    print("🚂 Railway detected - applying production settings")

    # Production settings override
    DEBUG = False

    # Railway provides these automatically
    ALLOWED_HOSTS = [
        '.railway.app',
        '.up.railway.app',
        'healthcheck.railway.app',  # Required for Railway health checks
        'localhost',
        '127.0.0.1'
    ]

    # Only optimize database if DATABASE_URL exists
    if DATABASE_URL:
        # Optimize database connections for Railway's memory limits
        DATABASES['default']['CONN_MAX_AGE'] = 60
        # Remove invalid MAX_CONNS option - not a valid PostgreSQL parameter
        DATABASES['default']['OPTIONS'] = {}

        print(f"✅ Railway PostgreSQL configuration:")
        print(f"   Host: {DATABASES['default']['HOST']}")
        print(f"   Port: {DATABASES['default']['PORT']}")
        print(f"   Database: {DATABASES['default']['NAME']}")
        print(f"   User: {DATABASES['default']['USER']}")
    else:
        print("⚠️  DATABASE_URL missing - PostgreSQL service not connected")
        print("   Add PostgreSQL service in Railway dashboard")
        print("   Railway will auto-create DATABASE_URL environment variable")

        # Use a placeholder database config to prevent crashes
        # This allows the app to start and show helpful error messages
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '/tmp/temp.db',  # Temporary SQLite for Railway startup
            }
        }
        print("   Using temporary SQLite database until PostgreSQL is connected")
    # Static files with WhiteNoise (add to beginning of middleware)
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
        MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + list(MIDDLEWARE)

    # Static files configuration
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Ensure staticfiles directory exists
    import pathlib
    pathlib.Path(STATIC_ROOT).mkdir(parents=True, exist_ok=True)

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
else:
    print("⚠️  Railway not detected - using local configuration")

