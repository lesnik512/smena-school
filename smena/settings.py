import os
# import raven
import raven as raven
from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Internationalization(object):
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'Asia/Yekaterinburg'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True


class Base(Internationalization, Configuration):
    SECRET_KEY = '6gju!5j-)_4wcmn1=@6o7x#ov45==35z9mz9%02xpu+a^4pved'
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'main',
        'dishes',
    ]
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'main.middlewares.BasketMiddleware',
    ]
    ROOT_URLCONF = 'smena.urls'
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'main.utils.get_basket',
                ],
            },
        },
    ]
    WSGI_APPLICATION = 'smena.wsgi.application'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
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
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


class Dev(Base):
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']
    INTERNAL_IPS = {'127.0.0.1'}
    Base.INSTALLED_APPS.extend([
        'debug_toolbar'
    ])
    Base.MIDDLEWARE.extend([
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ])


class Prod(Base):
    DEBUG = False
    ALLOWED_HOSTS = ['ash.redeploy.ru']
    Base.INSTALLED_APPS.extend([
        'raven.contrib.django.raven_compat'
    ])
    Base.MIDDLEWARE.extend([
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ])
    RAVEN_CONFIG = {
        'dsn': 'http://7a60d6cdab6c42c9ae850b3deca67a3a:6551acd7d0f84f0d98ebf2655bea80c9@sentry.smenatest.ru/63',
        'release': raven.fetch_git_sha(os.path.dirname(os.pardir))
    }
