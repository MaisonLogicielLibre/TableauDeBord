# coding: utf-8

"""
Django settings for TableauDeBord.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n!01nl+318#x75_%le8#s0=-*ysw&amp;y49uc#t=*wvi(9hnyii0z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Application definition
CRISPY_TEMPLATE_PACK = 'bootstrap'

INSTALLED_APPS = (
    'bootstrap3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_filters',
    'crispy_forms',
    'embed_video',
    'app.home',
    'app.company',
    'app.founder',
    'app.mentor',
    'app.kpi',
    'app.experiment',
    'app.businessCanvas',
    'app.finance',
    'app.valuePropositionCanvas',
    'app.kanboard'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   "django.core.context_processors.i18n",
   "django.contrib.auth.context_processors.auth",
   "app.home.context_processors.company_select",
   "app.home.context_processors.app_settings",
   'django.core.context_processors.request',
   'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'centech2.urls'

WSGI_APPLICATION = 'centech2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'centech_dashboard',                      # Or path to database file if using sqlite3.
        'USER': 'centech',                      # Not used with sqlite3.
        'PASSWORD': 'centech',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

TIME_ZONE = 'UTC'

USE_TZ = False #todo add timezone support


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/user/login'
LOGOUT_URL = '/user/logout'
LOGIN_REDIRECT_URL = '/company'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'app/home/templates'),
    os.path.join(BASE_DIR, 'app/company/templates'),
    os.path.join(BASE_DIR, 'app/experiment/templates'),
    os.path.join(BASE_DIR, 'app/founder/templates'),
    os.path.join(BASE_DIR, 'app/home/templates'),
    os.path.join(BASE_DIR, 'app/kpi/templates'),
    os.path.join(BASE_DIR, 'app/mentor/templates'),
    os.path.join(BASE_DIR, 'app/businessCanvas/templates'),
    os.path.join(BASE_DIR, 'app/finance/templates'),
    os.path.join(BASE_DIR, 'app/valuePropositionCanvas/templates'),
    os.path.join(BASE_DIR, 'app/kanboard/templates'),
    os.path.join(BASE_DIR, 'templates'),
)

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Restrict access to todo lists/views to `is_staff()` users.
# False here falls back to `is_authenticated()` users.
TODO_STAFF_ONLY = True

# If you use the "public" ticket filing option, to whom should these tickets be assigned?
# Must be a valid username in your system. If unset, unassigned tickets go to the first superuser.
TODO_DEFAULT_ASSIGNEE = 'admin'

# If you use the "public" ticket filing option, to which list should these tickets be saved?
# Defaults to first list found, which is probably not what you want!
TODO_DEFAULT_LIST_ID = 23

# If you use the "public" ticket filing option, to which *named URL* should the user be
# redirected after submitting? (since they can't see the rest of the ticket system).
# Defaults to "/"
TODO_PUBLIC_SUBMIT_REDIRECT = '/'

########################################################
#                 Internationalisation                 #
########################################################

LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

#not import the real utils here! We don't want an infiny loop
gettext = lambda x: x

#List of supported languages
LANGUAGES = (
   ('fr', gettext('French')),
   ('en', gettext('English')),
   ('pt', gettext('Portuguese'))
)

#List of translation directory
LOCALE_PATHS = (
    'app/company/locale/',
    'app/mentor/locale/',
    'app/founder/locale/',
    'app/home/locale/',
    'app/kpi/locale/',
    'app/experiment/locale/',
    'app/businessCanvas/locale/',
    'app/finance/locale/',
    'app/valuePropositionCanvas/locale/',
    'app/kanboard/locale/'
)


DASHBOARD_APP = {
    'site': {
        'name': u"TableauDeBord",
        'litteral_name': u"Tableau de Bord",
        'url': u"http://127.0.0.1:8000",
        'dns': u"kpi.etsmtl.ca",
        'email_technique': u"support.centech@etsmtl.ca",
        'repository': u"https://github.com/MaisonLogicielLibre/TableauDeBord",
        'bugtracker': u"https://github.com/MaisonLogicielLibre/TableauDeBord/issues",
        'entreprise': {
            'name': u"Centech",
            'address': u"400 rue Montfort, local C-1100, Montréal (Québec) H3C 4J9",
            'phone': u"514 396-8552"
        },
        'social': {
            'twitter': u'https://twitter.com/centechmtl',
            'facebook': u'https://www.facebook.com/etscentech?ref=ts&fref=ts',
            'linkedin': u'https://www.linkedin.com/grp/home?gid=2741468&sort=POPULAR',
            'youtube': u'https://www.youtube.com/channel/UCBE0aabDceUdOvd_NtX-jig'
        },
    }
}

BOOTSTRAP3 = {
   # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    'success_css_class': '',
}