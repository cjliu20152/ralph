# -*- coding: utf-8 -*-
import json
import os
from collections import ChainMap

from django.contrib.messages import constants as messages


def bool_from_env(var, default: bool=False) -> bool:
    """Helper for converting env string into boolean.

    Returns bool True for string values: '1' or 'true', False otherwise.
    """
    def str_to_bool(s: str) -> bool:
        return s.lower() in ('1', 'true')

    os_var = os.environ.get(var)
    if os_var is None:
        # as user expect
        return default
    else:
        return str_to_bool(os_var)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'CHANGE_ME')
LOG_FILEPATH = os.environ.get('LOG_FILEPATH', '/tmp/ralph.log')

DEBUG = False

ALLOWED_HOSTS = ['*']

# Only for deployment
RALPH_INSTANCE = os.environ.get('RALPH_INSTANCE', 'http://127.0.0.1:8000')

# Application definition

INSTALLED_APPS = (
    'ralph.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_rq',
    'import_export',
    'mptt',
    'reversion',
    'sitetree',
    'ralph.accounts',
    'ralph.assets',
    'ralph.attachments',
    'ralph.back_office',
    'ralph.dashboards',
    'ralph.data_center',
    'ralph.dhcp',
    'ralph.deployment',
    'ralph.licences',
    'ralph.domains',
    'ralph.supports',
    'ralph.security',
    'ralph.lib.foundation',
    'ralph.lib.table',
    'ralph.networks',
    'ralph.data_importer',
    'ralph.dc_view',
    'ralph.reports',
    'ralph.virtual',
    'ralph.operations',
    'ralph.lib.external_services',
    'ralph.lib.transitions',
    'ralph.lib.permissions',
    'ralph.lib.custom_fields',
    'rest_framework',
    'rest_framework.authtoken',
    'taggit',
    'taggit_serializer',
    'ralph.ralph2_sync',
)

RALPH2_RALPH3_CROSS_VALIDATION_ENABLED = bool_from_env(
    'RALPH2_RALPH3_CROSS_VALIDATION_ENABLED'
)
if RALPH2_RALPH3_CROSS_VALIDATION_ENABLED:
    RALPH2_PREVIEW_PREFIX_URL = os.environ.get(
        'RALPH2_PREVIEW_PREFIX_URL', 'http://ralph2.localhost/admin'
    )
    INSTALLED_APPS += (
        'ralph.cross_validator',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ralph.urls'
URLCONF_MODULES = [ROOT_URLCONF]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'ralph.lib.template.loaders.AppTemplateLoader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'ralph.wsgi.application'

MYSQL_OPTIONS = {
    'sql_mode': 'TRADITIONAL',
    'charset': 'utf8',
    'init_command': """
    SET storage_engine=INNODB;
    SET character_set_connection=utf8,collation_connection=utf8_unicode_ci;
    SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
    """
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME', 'ralph_ng'),
        'USER': os.environ.get('DATABASE_USER', 'ralph_ng'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'ralph_ng') or None,
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASE_PORT', 3306),
        'OPTIONS': MYSQL_OPTIONS,
        'ATOMIC_REQUESTS': True,
        'TEST': {
            'NAME': 'test_ralph_ng',
        }
    }
}

AUTH_USER_MODEL = 'accounts.RalphUser'
LOGIN_URL = '/login/'

LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'admin', 'static'),
)
STATIC_ROOT = os.environ.get(
    'STATIC_ROOT', os.path.join(BASE_DIR, 'var', 'static')
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get(
    'MEDIA_ROOT', os.path.join(BASE_DIR, 'var', 'media')
)

# adapt message's tags to bootstrap
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.ERROR: 'alert',
}

DEFAULT_DEPRECIATION_RATE = int(os.environ.get('DEFAULT_DEPRECIATION_RATE', 25))  # noqa
CHECK_IP_HOSTNAME_ON_SAVE = bool_from_env('CHECK_IP_HOSTNAME_ON_SAVE', True)
ASSET_HOSTNAME_TEMPLATE = {
    'prefix': '{{ country_code|upper }}{{ code|upper }}',
    'postfix': '',
    'counter_length': 5,
}
DEFAULT_COUNTRY_CODE = os.environ.get('DEFAULT_COUNTRY_CODE', 'POL')


LDAP_SERVER_OBJECT_USER_CLASS = 'user'  # possible values: user, person

ADMIN_SITE_HEADER = 'Ralph 3'
ADMIN_SITE_TITLE = 'Ralph 3'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'datefmt': '%d.%m.%Y %H:%M:%S',
            'format': (
                '[%(asctime)08s,%(msecs)03d] %(levelname)-7s [%(processName)s'
                ' %(process)d] %(module)s - %(message)s'),
        },
        'simple': {
            'datefmt': '%H:%M:%S',
            'format': '[%(asctime)08s] %(levelname)-7s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 10,
            'filename': os.environ.get(
                'LOG_FILEPATH', LOG_FILEPATH
            ),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': os.environ.get('LOGGING_DJANGO_REQUEST_LEVEL', 'WARNING'),
            'propagate': True,
        },
        'ralph': {
            'handlers': ['file'],
            'level': os.environ.get('LOGGING_RALPH_LEVEL', 'WARNING'),
            'propagate': True,
        },
        'rq.worker': {
            'level': os.environ.get('LOGGING_RQ_LEVEL', 'WARNING'),
            'handlers': ['file'],
            'propagate': True,
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'ralph.lib.permissions.api.RalphPermission',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'ralph.lib.permissions.api.PermissionsForObjectFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # noqa
    'PAGE_SIZE': 10,
    'DEFAULT_METADATA_CLASS': 'ralph.lib.api.utils.RalphApiMetadata',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',  # noqa
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ('v1',)
}

REDIS_CONNECTION = {
    'HOST': os.environ.get('REDIS_HOST', 'localhost'),
    'PORT': os.environ.get('REDIS_PORT', '6379'),
    'DB': int(os.environ.get('REDIS_DB', 0)),
    'PASSWORD': os.environ.get('REDIS_PASSWORD', ''),
}

# set to False to turn off cache decorator
USE_CACHE = bool_from_env('USE_CACHE', True)

SENTRY_ENABLED = bool_from_env('SENTRY_ENABLED')
SENTRY_JS_DSN = os.environ.get('SENTRY_JS_DSN', None)
SENTRY_JS_CONFIG = json.loads(os.environ.get('SENTRY_JS_CONFIG', '{}'))

BACK_OFFICE_ASSET_AUTO_ASSIGN_HOSTNAME = True

TAGGIT_CASE_INSENSITIVE = True  # case insensitive tags

RQ_QUEUES = {
    'default': dict(
        **REDIS_CONNECTION
    )
}
RALPH_QUEUES = {
    'ralph_ext_pdf': {},
    'ralph_async_transitions': {
        'DEFAULT_TIMEOUT': 3600,
    },
}
for queue_name, options in RALPH_QUEUES.items():
    RQ_QUEUES[queue_name] = ChainMap(RQ_QUEUES['default'], options)


RALPH_EXTERNAL_SERVICES = {
    'PDF': {
        'queue_name': 'ralph_ext_pdf',
        'method': 'inkpy_jinja.pdf',
    },
}

RALPH_INTERNAL_SERVICES = {
    'ASYNC_TRANSITIONS': {
        'queue_name': 'ralph_async_transitions',
        'method': 'ralph.lib.transitions.async.run_async_transition'
    }
}

# =============================================================================
# Deployment
# =============================================================================

DEPLOYMENT_MAX_DNS_ENTRIES_TO_CLEAN = 30

# =============================================================================

# Example:
# MY_EQUIPMENT_LINKS = [
#     {'url': 'http://....', 'name': 'Link name'},
# ]
MY_EQUIPMENT_LINKS = json.loads(os.environ.get('MY_EQUIPMENT_LINKS', '[]'))
MY_EQUIPMENT_REPORT_FAILURE_URL = os.environ.get('MY_EQUIPMENT_REPORT_FAILURE_URL', '')  # noqa
MY_EQUIPMENT_SHOW_BUYOUT_DATE = bool_from_env('MY_EQUIPMENT_SHOW_BUYOUT_DATE')

# Sets URL shown to user if they declare that they dp not have specific asset.
MISSING_ASSET_REPORT_URL = os.environ.get('MISSING_ASSET_REPORT_URL', None)

# Stocktaking tagging config - each variable describes individual tag.
# To disable tag set it to None or, in case of date tag, set variable to '0'.
INVENTORY_TAG = os.environ.get('INVENTORY_TAG', 'INV')
# This tag means user himself confirmed asset possession.
INVENTORY_TAG_USER = os.environ.get('INVENTORY_TAG_USER', 'INV_CONF')
INVENTORY_TAG_MISSING = os.environ.get('INVENTORY_TAG_MISSING', 'INV_MISSING')
INVENTORY_TAG_APPEND_DATE = bool_from_env('INVENTORY_TAG_APPEND_DATE', True)

MAP_IMPORTED_ID_TO_NEW_ID = False

OPENSTACK_INSTANCES = json.loads(os.environ.get('OPENSTACK_INSTANCES', '[]'))

# issue tracker url for Operations urls (issues ids) - should end with /
ISSUE_TRACKER_URL = os.environ.get('ISSUE_TRACKER_URL', '')

# Networks
DEFAULT_NETWORK_BOTTOM_MARGIN = int(os.environ.get('DEFAULT_NETWORK_BOTTOM_MARGIN', 10))  # noqa
DEFAULT_NETWORK_TOP_MARGIN = int(os.environ.get('DEFAULT_NETWORK_TOP_MARGIN', 0))  # noqa
# deprecated, to remove in the future
DEFAULT_NETWORK_MARGIN = int(os.environ.get('DEFAULT_NETWORK_MARGIN', 10))
# when set to True, network records (IP/Ethernet) can't be modified until
# 'expose in DHCP' is selected
DHCP_ENTRY_FORBID_CHANGE = bool_from_env('DHCP_ENTRY_FORBID_CHANGE', True)

# enable integration with DNSaaS, for details see
# https://github.com/allegro/django-powerdns-dnssec
ENABLE_DNSAAS_INTEGRATION = bool_from_env('ENABLE_DNSAAS_INTEGRATION')
DNSAAS_URL = os.environ.get('DNSAAS_URL', '')
DNSAAS_TOKEN = os.environ.get('DNSAAS_TOKEN', '')
DNSAAS_AUTO_PTR_ALWAYS = os.environ.get('DNSAAS_AUTO_PTR_ALWAYS', 2)
DNSAAS_AUTO_PTR_NEVER = os.environ.get('DNSAAS_AUTO_PTR_NEVER', 1)
# user in dnsaas which can do changes, like update TXT records etc.
DNSAAS_OWNER = os.environ.get('DNSAAS_OWNER', 'ralph')
# pyhermes topic where messages about auto txt records are announced
DNSAAS_AUTO_TXT_RECORD_TOPIC_NAME = os.environ.get(
    'DNSAAS_AUTO_TXT_RECORD_TOPIC_NAME', None
)
# define names of values send to DNSAAS for:
# DataCenterAsset, Cluster, VirtualServer
DNSAAS_AUTO_TXT_RECORD_PURPOSE_MAP = {
    # self.configuration_path.class will be send as 'VENTURE'
    'class_name': 'VENTURE',
    # self.configuration_path.module will be send as 'ROLE'
    'module_name': 'ROLE',
    # self.configuration_path.path will be send as 'PATH'
    'configuration_path': 'CONFIGURATION_PATH',
    # self.service_env will be send as 'SERVICE_ENV'
    'service_env': 'SERVICE_ENV',
    # self.model will be send as 'MODEL'
    'model': 'MODEL',
    # self.location will be send as 'LOCATION'
    'location': 'LOCATION',
    # self.location will be send as 'LOCATION'
    # if any of above is set to none
    # 'location': None
    # then this value won't be set at all
}

if ENABLE_DNSAAS_INTEGRATION:
    INSTALLED_APPS += (
        'ralph.dns',
    )


ENABLE_HERMES_INTEGRATION = bool_from_env('ENABLE_HERMES_INTEGRATION')
HERMES = json.loads(os.environ.get('HERMES', '{}'))
HERMES['ENABLED'] = ENABLE_HERMES_INTEGRATION
# topic name where DC asset, cloud host, virtual server changes should be
# announced
HERMES_HOST_UPDATE_TOPIC_NAME = os.environ.get(
    'HERMES_HOST_UPDATE_TOPIC_NAME', None
)

if ENABLE_HERMES_INTEGRATION:
    INSTALLED_APPS += (
        'pyhermes.apps.django',
    )


RALPH2_HERMES_SYNC_ENABLED = bool_from_env('RALPH2_HERMES_SYNC_ENABLED')
RALPH2_HERMES_SYNC_FUNCTIONS = json.loads(
    os.environ.get('RALPH2_HERMES_SYNC_FUNCTIONS', '[]')
)

# mapping model's name to type
RALPH2_RALPH3_VIRTUAL_SERVER_TYPE_MAPPING = json.loads(
    os.environ.get('RALPH2_RALPH3_VIRTUAL_SERVER_TYPE_MAPPING', '{}')
)
RALPH2_HERMES_ROLE_PROPERTY_WHITELIST = json.loads(
    os.environ.get('RALPH2_HERMES_ROLE_PROPERTY_WHITELIST', '[]')
)
ENABLE_SAVE_DESCENDANTS_DURING_NETWORK_SYNC = bool_from_env(
    'ENABLE_SAVE_DESCENDANTS_DURING_NETWORK_SYNC', True
)
