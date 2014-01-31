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

from devops.models import NodeControl, Node
from devops.helpers.decorators import singleton


@singleton
class DriverManager():
    pool = {}
    driver = None

    def __init__(self, driver=None):
        self.driver = import_module(driver or settings.DRIVER)
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

    def get_first_control_driver(self):
        return self.pool[:1]

    def disconnect(self, name=None):
        if name:
            self.pool[name].close()
        else:
            for driver in self.pool:
                driver.__del__()

    def node_active(self, node):
        nc = NodeControl.objects.get(node__name=node)
        return self.pool[nc.name].node_active(node=node)

    def node_create(self, node, node_control=None):
        if node_control:
            self.pool[node_control].node_create(node=node)
        else:
            self.get_random_control_driver().node_create(node=node)

    def node_create_snapshot(self, node, name, description):
        nc = NodeControl.objects.get(node__name=node.name)
        self.pool[nc.name].node_create_snapshot(
            node=node,
            name=name,
            description=description
        )

    def node_delete_snapshot(self, node, name=None):
        nc = NodeControl.objects.get(node__name=node.name)
        self.pool[nc.name].node_delete_snapshot(node=node, name=name)


    def node_list(self):
        return_list = []
        for node in self.pool.keys():
            return_list.append(self.pool[node].node_list())

        return return_list

    def node_revert_snapshot(self, node, name=None):
        nc = NodeControl.objects.get(node__name=node.name)
        self.pool[nc.name].node_revert_snapshot(node=node, name=name)


    def node_snapshot_exists(self, node, name):
        pass

    def node_suspend(self, node):
        pass

    def node_undefine_by_name(self, name):
        pass

    def network_create(self, network):
        for driver in self.pool:
            driver.network_create(network=network)

    def network_destroy(self, network):
        for driver in self.pool:
            driver.network_destroy(network=network)

    def network_undefine(self, network):
        for driver in self.pool:
            driver.network_undefine(network=network)

    def node_get_vnc_port(self, node):
        pass
