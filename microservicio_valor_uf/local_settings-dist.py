'''
    Local settings
'''
import os


from .settings import INSTALLED_APPS, BASE_DIR


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Apps to developer
DEV_APPS = []

# Final installed apps
INSTALLED_APPS += DEV_APPS

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
