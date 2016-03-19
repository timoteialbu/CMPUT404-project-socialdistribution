# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# openshift is our PAAS for now.
ON_PAAS = 'OPENSHIFT_REPO_DIR' in os.environ

if ON_PAAS:
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ')_7av^!cy(wfx=k#3*7x+(=j^fzv+ot^1@sh9s9t=8$bu@r(z$'

# SECURITY WARNING: don't run with debug turned on in production!
# adjust to turn off when on Openshift, but allow an environment variable to override on PAAS
DEBUG = not ON_PAAS
DEBUG = DEBUG or os.getenv("debug","false").lower() == "true"

if ON_PAAS and DEBUG:
    print("*** Warning - Debug mode is on ***")

TEMPLATE_DEBUG = True

if ON_PAAS:
    ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS'], socket.gethostname()]
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'posts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The Django sites framework is required
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    #'allauth.socialaccount.providers.amazon',
    #'allauth.socialaccount.providers.angellist',
    #'allauth.socialaccount.providers.bitbucket',
    #'allauth.socialaccount.providers.bitly',
    #'allauth.socialaccount.providers.coinbase',
    #'allauth.socialaccount.providers.dropbox',
    #'allauth.socialaccount.providers.dropbox_oauth2',
    #'allauth.socialaccount.providers.edmodo',
    #'allauth.socialaccount.providers.evernote',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.flickr',
    #'allauth.socialaccount.providers.feedly',
    #'allauth.socialaccount.providers.fxa',
    #'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.hubic',
    #'allauth.socialaccount.providers.instagram',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.linkedin_oauth2',
    #'allauth.socialaccount.providers.odnoklassniki',
    #'allauth.socialaccount.providers.openid',
    #'allauth.socialaccount.providers.persona',
    #'allauth.socialaccount.providers.soundcloud',
    #'allauth.socialaccount.providers.spotify',
    #'allauth.socialaccount.providers.stackexchange',
    #'allauth.socialaccount.providers.tumblr',
    #'allauth.socialaccount.providers.twitch',
    #'allauth.socialaccount.providers.twitter',
    #'allauth.socialaccount.providers.vimeo',
    #'allauth.socialaccount.providers.vk',
    #'allauth.socialaccount.providers.weibo',
    #'allauth.socialaccount.providers.xing'
    'friendship',
    'rest_framework',
    'api',
)

# This ID comes from the Django admin page
# After adding a new site, click on it. Look in the browsers
# address space and there will be '/#/' where # is an int
# Set this # to the SITE_ID variable below
SITE_ID = 2

# After log in go to this webpage
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/account/login"

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

ACCOUNT_SIGNUP_FORM_CLASS = "mysite.forms.SignupForm"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Already defined Django-related contexts here

                # `allauth` needs this from django
                'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
)


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.IsAuthenticated',
    ],
    #'DEFAULT_PAGINATION_CLASS':
    #    'CMPUT404-project-socialdistribution.api.pagination.CustomPagination',
    #'PAGE_SIZE': 100,

    #'DEFAULT_PAGINATION_CLASS':
    #    'CMPUT404-project-socialdistribution.api.pagination.CustomPagination',
    #'PAGE_SIZE': 100
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10


}


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases




######CHANGE!!! Run my_setup.py

MEDIA_ROOT = '/home/kyle/Documents/cmput404/CMPUT404-project-socialdistribution/media/'

MEDIA_URL = '/media/'



if ON_PAAS:
    # determine if we are on MySQL or POSTGRESQL
    if "OPENSHIFT_POSTGRESQL_DB_USERNAME" in os.environ:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME':     os.environ['OPENSHIFT_APP_NAME'],
                'USER':     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
                'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
                'HOST':     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
                'PORT':     os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
            }
        }

    elif "OPENSHIFT_MYSQL_DB_USERNAME" in os.environ:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME':     os.environ['OPENSHIFT_APP_NAME'],
                'USER':     os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
                'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
                'HOST':     os.environ['OPENSHIFT_MYSQL_DB_HOST'],
                'PORT':     os.environ['OPENSHIFT_MYSQL_DB_PORT'],
            }
        }


else:
    # stock django, local development.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'MST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'wsgi','static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,"static"),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)
