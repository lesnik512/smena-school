import os
# import raven
from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Internationalization(object):
    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/
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
        # 'raven.contrib.django.raven_compat',
        # 'debug_toolbar',
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
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # 'debug_toolbar.middleware.DebugToolbarMiddleware',
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


class Dev(Base):
    DEBUG = True
    DEBUG_TOOLBAR = False
    STATICFILES_DIRS = [os.path.join(os.path.join(BASE_DIR, "static"))]


class Prod(Base):
    DEBUG = False
    DEBUG_TOOLBAR = False
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    ALLOWED_HOSTS = ['ash.redeploy.ru']



# RAVEN_CONFIG = {
#     'dsn': 'http://7a60d6cdab6c42c9ae850b3deca67a3a:6551acd7d0f84f0d98ebf2655bea80c9@sentry.smenadev.ru/63',
#     'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
# }

# INTERNAL_IPS = {'127.0.0.1'}
