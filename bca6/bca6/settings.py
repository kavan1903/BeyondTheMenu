"""
Django settings for bca6 project.
"""

from pathlib import Path
import os
# from dotenv import load_dotenv

# Load environment variables from .env file (create one if not already)
# load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-x0355rm9#!cq+fc2_0bh!^*_&dy!z0grdd(dm4%@45-o^ool-!')
DEBUG = True

ALLOWED_HOSTS = ['*']

# Installed applications
INSTALLED_APPS = [
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_panel',
    
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL configuration
ROOT_URLCONF = 'bca6.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Corrected path
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.cart_count',  # Add this line
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'bca6.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'beyondthemenu',
        'USER': 'root',
        'PASSWORD': os.getenv('DB_PASSWORD', 'Kavan@123'),  # Secure database password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Authentication settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # Static files for development
STATIC_ROOT = BASE_DIR / "staticfiles"  # Where collectstatic will store files

# Media files configuration
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Custom user model
AUTH_USER_MODEL = 'home.UserProfile'  # Ensure UserProfile model exists in home/models.py

# Email configuration (Use environment variables for security)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'malharexoticaa@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'dxzrofmzitovcyhs')



# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 3600  # 1 hour

# Jazzmin admin panel customization
JAZZMIN_SETTINGS = {
    "site_title": "Beyond The Menu Admin",
    "site_header": "Beyond The Menu",
    "site_brand": "Beyond The Menu",
    "welcome_sign": "Welcome to Beyond The Menu Admin Panel",
    "search_model": ["home.Category", "home.Subcategory", "home.MenuItem"],

    # Top menu links
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Dashboard", "url": "admin_dashboard", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "home"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["home", "auth"],

    # Sidebar Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "home.Category": "fas fa-folder",
        "home.Subcategory": "fas fa-list",
        "home.MenuItem": "fas fa-utensils",
    },

    "changeform_format": "horizontal_tabs",

    # Theme settings
    "theme": "darkly",
    "custom_css": "admin/css/custom_admin.css",
}

#payment
RAZORPAY_KEY_ID = "rzp_test_0WbOhBkylhz7hr"
RAZORPAY_KEY_SECRET = "ayWGihbLUtuitl7UkNzdXNr8"
