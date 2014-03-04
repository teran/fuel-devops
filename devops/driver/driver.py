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

import logging
import random

from django.utils.importlib import import_module
from django.conf import settings

from devops.helpers.decorators import singleton, debug

logger = logging.getLogger(__name__)
logwrap = debug(logger)

@singleton
class DriverManager():
    pool = {}
    driver = None

    @logwrap
    def __init__(self, driver=None):
        logger.info('DriverManager initialized')
        self.driver = import_module(driver or settings.DRIVER)
        for k in settings.CONTROL_NODES.keys():
            if not self.pool.get(k):
                self.pool[k] = self.driver.DevopsDriver(
                    **settings.CONTROL_NODES[k]
                )

    @logwrap
    def get_allocated_networks(self):
        allocated_networks = set()
        for i in self.pool.keys():
            for k in self.pool.get(i).get_allocated_networks():
                allocated_networks.add(k)

        return allocated_networks

    @logwrap
    def get_control_driver(self, name):
        return self.pool[name]

    @logwrap
    def get_random_control_driver(self):
        return self.pool[random.choice(self.pool.keys())]

    @logwrap
    def get_first_control_driver(self):
        return self.pool[:1]

    @logwrap
    def get_control_driver_by_node_name(self, node_name):
        nc = NodeControl.objects.get(node__name=node.name)
        return self.pool[nc.name]

    @logwrap
    def disconnect(self, name=None):
        if name:
            self.pool[name].close()
        else:
            for driver in self.pool:
                driver.__del__()

    @logwrap
    def node_active(self, node):
        self.get_control_driver_by_node_name(
            node.name
        ).node_active(node=node)

    @logwrap
    def node_create(self, node, node_control=None):
        if node_control:
            self.pool[node_control].node_create(node=node)
        else:
            self.get_random_control_driver().node_create(node=node)

    @logwrap
    def node_create_snapshot(self, node, name, description):
        self.get_control_driver_by_node_name(node.name).node_create_snapshot(
            node=node,
            name=name,
            description=description
        )

    @logwrap
    def node_delete_snapshot(self, node, name=None):
        self.get_control_driver_by_node_name(
            node.name
        ).node_delete_snapshot(node=node, name=name)

    @logwrap
    def node_list(self):
        return_list = []
        for node in self.pool.keys():
            return_list.append(self.pool[node].node_list())

        return return_list

    @logwrap
    def node_revert_snapshot(self, node, name=None):
        self.get_control_driver_by_node_name(
            node.name
        ).node_revert_snapshot(node=node, name=name)

    @logwrap
    def node_snapshot_exists(self, node, name):
        self.get_control_driver_by_node_name(
            node.name
        ).node_snapshot_exists(node, name)

    @logwrap
    def node_suspend(self, node):
        pass

    @logwrap
    def node_undefine_by_name(self, name):
        pass

    @logwrap
    def network_create(self, network):
        for driver in self.pool:
            driver.network_create(network=network)

    @logwrap
    def network_destroy(self, network):
        for driver in self.pool:
            driver.network_destroy(network=network)

    @logwrap
    def network_undefine(self, network):
        for driver in self.pool:
            driver.network_undefine(network=network)

    @logwrap
    def node_get_vnc_port(self, node):
        pass

    @logwrap
    def volume_capacity(self, volume):
        return self.pool.get(volume.node_control.name).volume_capacity(volume)

    def volume_path(self, volume):
        return self.pool.get(volume.node_control.name).volume_path(volume)