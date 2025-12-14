from os import environ

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ.get('MYSQL_DATABASE'),
        'USER': environ.get('MYSQL_USER'),
        'PASSWORD': environ.get('MYSQL_PASSWORD'),
        'HOST': 'db',
        'PORT': 3306,
        'ATOMIC_REQUESTS': True,
    }
}

SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error', 'models.E025',
                          'fields.W903']

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '.comics.org',
    '.comics.org.',  # Allow FQDN and subdomains.  Can be dropped in 1.7
]

# Disable memcached for local development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Use database sessions instead of cached_db
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Disable Elasticsearch
USE_ELASTICSEARCH = False

# Disable debugging middleware that might hang
DEBUG = True

def _modify(settings):
    settings['INSTALLED_APPS'] += ('django_extensions',)
