#    Copyright 2013 - 2014 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from os import environ

OPENVSWITCH = True
NETWORK_VLAN_TAGS = range(100,200)

CONTROL_NODES = {
    'ishishkin-msk': {
        'driver': 'devops.driver.libvirt.libvirt_driver',
        'connection_string': 'qemu+tcp://127.0.0.1:16509/system',
        'storage_pool_name': 'default',
        'capacity': 11,
    },
    'mc0n3-msk.msk': {
        'driver': 'devops.driver.libvirt.libvirt_driver',
        'connection_string':
     'qemu+tcp://mc0n3-msk.msk.mirantis.net:16509/system',
        'storage_pool_name': 'default',
        'capacity': 7,
    },
}

INSTALLED_APPS = ['south', 'devops']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST_CHARSET': 'UTF8'
    }
}

SECRET_KEY = 'dummykey'

VNC_PASSWORD = environ.get('VNC_PASSWORD', None)

# Default timezone for clear logging
TIME_ZONE = 'UTC'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(funcName)s %(message)s'
        }
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'devops': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}

try:
    from local_settings import *  # noqa
except ImportError:
    pass
