from os import environ

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ.get('MYSQL_DATABASE'),
        'USER': environ.get('MYSQL_USER'),
        'PASSWORD': environ.get('MYSQL_PASSWORD'),
        'HOST': 'db',
        'PORT': 3306,
    }
}

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error', 'models.E025']

ALLOWED_HOSTS = [
    '0.0.0.0',
    '.comics.org',
    '.comics.org.',  # Allow FQDN and subdomains.  Can be dropped in 1.7
]

