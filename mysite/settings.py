# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = ')_7av^!cy(wfx=k#3*7x+(=j^fzv+ot^1@sh9s9t=8$bu@r(z$'

# SECURITY WARNING: don't run with debug turned on in production!
# adjust to turn off when on Openshift, but allow an environment variable to override on PAAS
DEBUG = True

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
	'posts',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admindocs',
	# The Django sites framework is required
	'django.contrib.sites',
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	# ... include the providers you want to enable:
	# 'allauth.socialaccount.providers.amazon',
	# 'allauth.socialaccount.providers.angellist',
	# 'allauth.socialaccount.providers.bitbucket',
	# 'allauth.socialaccount.providers.bitly',
	# 'allauth.socialaccount.providers.coinbase',
	# 'allauth.socialaccount.providers.dropbox',
	# 'allauth.socialaccount.providers.dropbox_oauth2',
	# 'allauth.socialaccount.providers.edmodo',
	# 'allauth.socialaccount.providers.evernote',
	# 'allauth.socialaccount.providers.facebook',
	# 'allauth.socialaccount.providers.flickr',
	# 'allauth.socialaccount.providers.feedly',
	# 'allauth.socialaccount.providers.fxa',
	# 'allauth.socialaccount.providers.github',
	# 'allauth.socialaccount.providers.google',
	# 'allauth.socialaccount.providers.hubic',
	# 'allauth.socialaccount.providers.instagram',
	# 'allauth.socialaccount.providers.linkedin',
	# 'allauth.socialaccount.providers.linkedin_oauth2',
	# 'allauth.socialaccount.providers.odnoklassniki',
	# 'allauth.socialaccount.providers.openid',
	# 'allauth.socialaccount.providers.persona',
	# 'allauth.socialaccount.providers.soundcloud',
	# 'allauth.socialaccount.providers.spotify',
	# 'allauth.socialaccount.providers.stackexchange',
	# 'allauth.socialaccount.providers.tumblr',
	# 'allauth.socialaccount.providers.twitch',
	# 'allauth.socialaccount.providers.twitter',
	# 'allauth.socialaccount.providers.vimeo',
	# 'allauth.socialaccount.providers.vk',
	# 'allauth.socialaccount.providers.weibo',
	# 'allauth.socialaccount.providers.xing'
	'friendship',
	'rest_framework',
	'rest_framework.authtoken',
	'api',
	'markdown_deux',
)

MARKDOWN_DEUX_STYLES = {
	"default": {
		"extras": {
			"code-friendly": None,
		},
		"safe_mode": "escape",
	},
}

# This ID comes from the Django admin page
# After adding a new site, click on it. Look in the browsers
# address space and there will be '/#/' where # is an int
# Set this # to the SITE_ID variable below
SITE_ID = 3

# After log in go to this webpage
LOGIN_REDIRECT_URL = "/posts/"
LOGIN_URL = "/account/login"
PUBLIC_URL = "/posts/"

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
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticated',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.BasicAuthentication',
		'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
	),
	'DEFAULT_PAGINATION_CLASS': 'api.pagination.CustomPagination'
}

JWT_AUTH = {
	'JWT_VERIFY_EXPIRATION': False,
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases




######CHANGE!!! Run my_setup.py

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# stock django, local development.
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

DATABASES['default'] =  dj_database_url.config()

WSGI_APPLICATION = 'mysite.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'MST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'wsgi', 'static')
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	os.path.join(PROJECT_ROOT, 'static/'),
)

STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(BASE_DIR, "static"),
	# os.path.join(os.path.dirname(__file__), 'static'),
)

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(BASE_DIR, 'templates'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
