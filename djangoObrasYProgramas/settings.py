"""
Django settings for djangoObrasYProgramas project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')*p06lu&+_ao^t6fefr!_3wcq#@m@17nkyrb3lye@=ot1kvrtb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'obras',
    'oauth2_provider',
    'smart_selects',
    # 'djangosecure',
    #'sslify',
)

# MIDDLEWARE_CLASSES = (
# 'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'oauth2_provider.middleware.OAuth2TokenMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# )

MIDDLEWARE_CLASSES = (
    #'sslify.middleware.SSLifyMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # Uncomment following if you want to access the admin
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'djangoObrasYProgramas.urls'

WSGI_APPLICATION = 'djangoObrasYProgramas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbobras1',
        'USER': 'obras',
        'PASSWORD': 'obras',
        'HOST': '',
        'PORT': '',
    }
}
IGNORE_MYSQL_WARNINGS = True
if IGNORE_MYSQL_WARNINGS:
    _GOT_FIRST_REQUEST = False
    def on_first_request(signal, sender):
        global _GOT_FIRST_REQUEST
        if not _GOT_FIRST_REQUEST:
            _GOT_FIRST_REQUEST = True

            from django.db.backends.mysql.base import CursorWrapper
            import MySQLdb as Database

            def _ignore_warnings(fn):
                def _execute(*args, **kwargs):
                    try:
                        return fn(*args, **kwargs)
                    except Database.Warning as e:
                        return None
                return _execute

            CursorWrapper.execute = _ignore_warnings(CursorWrapper.execute)
            CursorWrapper.executemany = _ignore_warnings(CursorWrapper.executemany)

    from django.core.signals import request_started
    request_started.connect(on_first_request)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

MEDIA_ROOT = os.path.join(BASE_DIR, 'obras/media')
MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SESSION_COOKIE_AGE = 35900
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_URL = '/admin/login/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/obrasapf/djangoObras/static'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'obras/templates/'),
)

TEMPLATETAGS_DIRS = (
    os.path.join(BASE_DIR, 'obras/templatetags/'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "obras/static/"),
)

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'edicomexsa@gmail.com'
EMAIL_HOST_PASSWORD = 'Edicomex2015'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

