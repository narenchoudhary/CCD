"""
Django settings for CCD project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x&uda4nsg--wxz*f630nb21-$wm+8e)$51m0^)y6)3rzxe8=u3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'iitg.ernet.in', '202.141.80.161',
                 '202.141.80.86']

AUTH_USER_MODEL = 'jobportal.UserProfile'

# Application definition


DJANGO_CONTRIB_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third party applications
# https://github.com/viewflow/django-material
# https://github.com/bruth/django-tracking2
# https://github.com/respondcreate/django-versatileimagefield
# https://github.com/un1t/django-cleanup
DJANGO_3RD_PARTY_APPS = [
    'material',
    'versatileimagefield',
    'django_cleanup',
    'tracking',
    'django_extensions',
]

PROJECT_APPS = [
    'internships',
    'jobportal',
    'mentormentee',
    'alumnijobs'
]

INSTALLED_APPS = DJANGO_CONTRIB_APPS + DJANGO_3RD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    # Add tracking MiddleWare before SessionMiddleware
    'tracking.middleware.VisitorTrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'CCD.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'CCD.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Sessions settings
# https://docs.djangoproject.com/en/1.9/ref/settings/#sessions
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_SECURE = True

# Remember session for one month
SESSION_COOKIE_AGE = 60*60*24*30

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-STATICFILES_DIRS

STATIC_URL = '/tnp/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')

# Media Files (Uploaded files)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/tnp/media/'

# File Upload Handlers
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

# Max upload size
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440

#########################################
# DEPLOYMENT SECURITY SETTINGS START HERE

# https://docs.djangoproject.com/en/1.9/ref/settings/#secure-content-type-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# https://docs.djangoproject.com/en/1.9/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/1.9/ref/settings/#csrf-cookie-httponly
#CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/1.9/ref/settings/#session-cookie-httponly
#SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/1.9/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'

#SECURE_PROXY_SSL_HEADER = False
#SECURE_SSL_REDIRECT = False

#CSRF_COOKIE_SECURE = True

#SESSION_COOKIE_SECURE = True
# DEPOLYMENT SECURITY SETTINGS END HERE
#########################################


# django-tracking2 settings
# https://github.com/bruth/django-tracking2#settings
TRACK_ANONYMOUS_USERS = False
TRACK_PAGEVIEWS = True
