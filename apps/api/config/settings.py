"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-_h@8w3@runrjwfg6u2b&kk9+qfq-8f4(x0e!mn6zf=iu!$*a@0')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,.vercel.app').split(',')


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'storages',
    
    # Local apps
    'blog',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Check for Neon database configuration first
PGHOST = config('PGHOST', default=None)
DATABASE_URL = config('DATABASE_URL', default=None)

if PGHOST or DATABASE_URL:
    # Use Neon serverless database configuration
    if DATABASE_URL:
        # Use DATABASE_URL if provided (recommended for Neon)
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=0)
        }
    else:
        # Use individual environment variables
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('PGDATABASE'),
                'USER': config('PGUSER'),
                'PASSWORD': config('PGPASSWORD'),
                'HOST': config('PGHOST'),
                'PORT': config('PGPORT', default=5432, cast=int),
                'OPTIONS': {
                    'sslmode': 'require',
                },
                'DISABLE_SERVER_SIDE_CURSORS': True,
            }
        }
    
    # Neon-specific connection settings
    DATABASES['default']['CONN_MAX_AGE'] = 0  # Close connections after each request
    DATABASES['default']['CONN_HEALTH_CHECKS'] = True  # Enable connection health checks
else:
    # Use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# AWS S3 Settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_SESSION_TOKEN = config('AWS_SESSION_TOKEN', default='')  # For temporary credentials
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'  # Make uploaded files publicly readable
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
    'ACL': 'public-read',  # Ensure objects are publicly readable
}
AWS_S3_FILE_OVERWRITE = False  # Don't overwrite files with same name
AWS_S3_VERIFY = True  # Verify SSL certificates
AWS_S3_USE_SSL = True  # Use HTTPS
AWS_QUERYSTRING_AUTH = False  # Use public URLs instead of signed URLs
AWS_QUERYSTRING_EXPIRE = 3600  # Signed URLs expire in 1 hour

# Storage Settings
# Check for Pulumi-provided static bucket name (for AWS deployment)
STATIC_BUCKET_NAME = config('STATIC_BUCKET_NAME', default='')

if STATIC_BUCKET_NAME:
    # Use S3 for static and media files when deployed via Pulumi
    AWS_STORAGE_BUCKET_NAME = STATIC_BUCKET_NAME
    AWS_S3_CUSTOM_DOMAIN = f'{STATIC_BUCKET_NAME}.s3.amazonaws.com'
    
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        },
    }
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
elif AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    # Use S3 for media files if AWS credentials are provided (existing setup)
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
else:
    # Use local storage for development
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Jazzmin Admin Theme Configuration
JAZZMIN_SETTINGS = {
    # Title on the login screen and main admin page
    "site_title": "CG Stewart Blog Admin",
    "site_header": "CG Stewart Blog",
    "site_brand": "CG Stewart",
    "site_logo": None,  # You can add a logo path here later
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to CG Stewart Blog Admin",
    "copyright": "CG Stewart",
    "search_model": ["blog.Post", "blog.Project"],
    "user_avatar": None,
    
    # Top Menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API", "url": "/api/v1/", "new_window": True},
        {"model": "blog.Post"},
        {"model": "blog.Project"},
    ],
    
    # User Menu
    "usermenu_links": [
        {"name": "API Overview", "url": "/api/v1/", "new_window": True},
        {"model": "auth.user"}
    ],
    
    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Custom Links
    "custom_links": {
        "blog": [{
            "name": "View API", 
            "url": "/api/v1/", 
            "icon": "fas fa-code",
            "permissions": ["blog.view_post"]
        }]
    },
    
    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "blog.Bio": "fas fa-user-circle",
        "blog.Post": "fas fa-blog",
        "blog.Video": "fas fa-video",
        "blog.Project": "fas fa-code-branch",
    },
    
    # Default Icons
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # UI Tweaks
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    
    # Change View
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

# Jazzmin UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
