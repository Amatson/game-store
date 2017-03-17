"""
Django settings for game_store project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
try:
    import gamestore.mailconfig as cf
except:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5a2e_b+5mgnvs-&x+(0)%ucdfcw$an)+2$i2^mnoj68a!gifqo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Added allowed hosts for heroku, and because of that also to localhosts
ALLOWED_HOSTS = [
    'nilkan-mikrosorto.herokuapp.com',
    'localhost'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gamestore',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'gamestore.middlewares.TimezoneMiddleware'
]

ROOT_URLCONF = 'gamestore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gamestore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# Added for the Heroku sake.
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Seller ID settings for Payment Verification
SID = 'katsonmirrinkolo'
SID_SECRET_KEY = 'd0a292a5c6f3b7a6a081860448cf21c7'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Set email host user and password for heroku and for local
if 'DYNO' in os.environ:
    EMAIL_HOST_USER = os.environ.get('HEROKU_EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('HEROKU_EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
  # Here might be good to have some error handling if mailconfig file cannot be imported, but as this should be run only in heroku or localhost, this should not be a problem.
    try:
        EMAIL_HOST_USER = cf.EMAIL_HOST_USER
        EMAIL_HOST_PASSWORD = cf.EMAIL_HOST_PASSWORD
        DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    except:
        pass


# Only when running in Heroku
if "DYNO" in os.environ:
    #STATIC_ROOT = 'staticfiles'
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    DEBUG = False # False, once service is succesfully deployed
    ALLOWED_HOSTS = ['*']

# Game categories for global variable
GAME_CATEGORIES = [
    '3D',
    'Action',
    'Adventure',
    'Board',
    'Card',
    'Driving',
    'Educational',
    'Fashion',
    'Fighting',
    'Horror',
    'Puzzle',
    'Shooting',
    'Simulator',
    'Sports',
    'Strategy',
]
