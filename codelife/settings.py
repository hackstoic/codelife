#encoding=utf-8
"""
Django settings for codelife project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = BASE_DIR
LOG_ROOT = "/var/log/codelife/"


try: 
    from private import SECRET_KEY, DATABASES
except Exception as ex:
    print ex



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = YOUR_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = True

# TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# APPEND_SLASH = False
# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # open django comment function dependency
    'django.contrib.comments',  # open django comment function,
    'blog',
    'DjangoUeditor',
    'wechat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'codelife.urls'

WSGI_APPLICATION = 'codelife.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases



# DATABASES = {
    # 'default': {
        # sqlite3 setting below
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # msyql setting below
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': MYSQL_DB_NAME,
        # 'USER': MYSQL_USER,
        # 'PASSWORD': MYSQL_PASSWORD,
        # 'HOST': MYSQL_HOST,
        # 'PORT': MYSQL_PORT
    # }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_PATH, "static/").replace("\\", '/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    ("css", os.path.join(STATIC_ROOT,'css')),
    ("js", os.path.join(STATIC_ROOT,'js')),
    ("images", os.path.join(STATIC_ROOT,'images')),
)

MEDIA_ROOT = os.path.join(PROJECT_PATH, "media/").replace("\\", '/')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\', '/'),

)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


# logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(process)d'
                      ' line:%(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(module)s '
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_ROOT, 'codelife.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'blog': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'wechat': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },

    },
}

