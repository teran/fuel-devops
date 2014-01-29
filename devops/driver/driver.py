#    Copyright 2014 Mirantis, Inc.
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

import random

from django.utils.importlib import import_module
from django.conf import settings

from devops.models import NodeControl


class DriverManager():
    pool = {}
    driver = None

    def __init__(self, driver):
        self.driver = import_module(settings.DRIVER)
        for k in settings.CONTROL_NODES.keys():
            nc, created = NodeControl.objects.get_or_create(
                connection_string=settings.CONTROL_NODES[k][
                    'connection_string']
            )

            if created:
                nc.name = k
                nc.save()

            if not self.pool.get(k):
                self.pool[k] = self.driver.DevopsDriver(
                    **settings.CONTROL_NODES[k]
                )

    def get_control_driver(self, name):
        return self.pool[name]

    def get_random_control_driver(self):
        return self.pool[random.choice(self.pool.keys())]

    def disconnect(self, name=None):
        if name:
            self.pool[name].close()
        else:
            for conn in self.pool.items():
                conn.close()
