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

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.importlib import import_module

from devops.helpers.decorators import singleton, debug

logger = logging.getLogger(__name__)
logwrap = debug(logger)

@singleton
class DriverManager():
    pool = {}

    @logwrap
    def __init__(self):
        logger.info('DriverManager initialized')
        for k in settings.CONTROL_NODES.keys():
            if not self.pool.get(k):
                driver = import_module(settings.CONTROL_NODES[k]['driver'])
                logger.info('Initializing %s instance' % driver)

                self.pool[k] = driver.DevopsDriver(
                    **settings.CONTROL_NODES[k])
                from devops.models import NodeControl, Environment
                env = Environment.objects.all()[0]
                nc, created = NodeControl.objects.get_or_create(
                    name=k,
                    connection_string=settings.CONTROL_NODES[k]['connection_string'],
                    pool=settings.CONTROL_NODES[k]['storage_pool_name'],
                    environment=env)
                nc.save()

    @logwrap
    def driver(self):
        return self.get_random_control_driver()

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
    def get_control_object_by_driver(self, driver):
        from devops.models import NodeControl
        return NodeControl.objects.get(
            connection_string=driver.connection_string)

    @logwrap
    def get_random_control_driver(self):
        return self.pool[random.choice(self.pool.keys())]

    @logwrap
    def get_first_control_driver(self):
        return self.pool.values()[0]

    @logwrap
    def get_control_driver_by_node_name(self, node_name):
        from devops.models import NodeControl
        try:
            nc = NodeControl.objects.get(node__name=node_name)
            return self.pool[nc.name]
        except ObjectDoesNotExist:
            return self.pool.values()[0]

    @logwrap
    def get_network_by_driver_object(self, driver, network):
        from devops.models import Network


        return Network.objects.get(
            #node_control=self.get_control_object_by_driver(driver),
            name=network.name,
        )

    @logwrap
    def disconnect(self, name=None):
        if name:
            self.pool[name].close()
        else:
            for driver in self.pool:
                driver.__del__()

    @logwrap
    def network_active(self, network):
        return self.pool[network.node_control.name].network_active(
            network=network)

    @logwrap
    def network_define(self, network):
        for driver in self.pool.values():
            driver.network_define(network=network)
            network.node_control = self.get_control_object_by_driver(driver)

    @logwrap
    def network_exists(self, network):
        for control in self.pool.keys():
            ret = self.pool[control].network_exists(network=network)

            if ret:
                return ret
        return True

    @logwrap
    def node_active(self, node):
        return self.get_control_driver_by_node_name(
            node.name
        ).node_active(node=node)

    @logwrap
    def node_create(self, node, node_control=None):
        if node_control:
            self.pool[node_control].node_create(node=node)
        else:
            self.driver().node_create(node=node)

    @logwrap
    def node_create_snapshot(self, node, name, description):
        return self.get_control_driver_by_node_name(
            node.name
        ).node_create_snapshot(
            node=node, name=name, description=description)

    @logwrap
    def node_delete_snapshot(self, node, name=None):
        return self.get_control_driver_by_node_name(
            node.name
        ).node_delete_snapshot(node=node, name=name)

    @logwrap
    def node_destroy(self, node):
        return self.get_control_driver_by_node_name(
            node.name
        ).node_destroy(node=node)

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
        return self.get_control_driver_by_node_name(
            node.name
        ).node_suspend(node=node)

    @logwrap
    def node_undefine(self, node, undefine_snapshots=False):
        return self.get_control_driver_by_node_name(
            node.name
        ).node_undefine(node, undefine_snapshots=undefine_snapshots)

    @logwrap
    def node_undefine_by_name(self, name):
        pass

    @logwrap
    def network_create(self, network):
        for driver in self.pool.values():
            try:
                self.get_network_by_driver_object(
                    network=network, driver=driver)
                driver.network_create(network=network)
            except:
                from devops.models import Network
                network.pk = None
                driver.network_create(network=network)

    @logwrap
    def network_destroy(self, network):
        for driver in self.pool.values():
            driver.network_destroy(network=network)

    def node_exists(self, node):
        for driver in self.pool.values():
            logger.debug('node_exists: %s' % driver)
            ne = driver.node_exists(node)

            if ne:
                return ne
        return False

    @logwrap
    def network_undefine(self, network):
        for driver in self.pool.values():
            driver.network_undefine(
                network=self.get_network_by_driver_object(
                    driver=driver, network=network))


    @logwrap
    def node_define(self, node):
        driver = self.get_random_control_driver()
        driver.node_define(node)
        node.node_control = self.get_control_object_by_driver(driver=driver)

    @logwrap
    def node_get_vnc_port(self, node):
        pass

    def node_send_keys(self, node, keys):
        for driver in self.pool.values():
            driver.node_send_keys(node, keys)

    @logwrap
    def volume_capacity(self, volume):
        return self.pool.get(volume.node_control.name).volume_capacity(volume)

    @logwrap
    def volume_define(self, volume, pool=None):
        for driver in self.pool.values():
            driver.volume_define(volume=volume, pool=pool)

    @logwrap
    def volume_delete(self, volume):
        for driver in self.pool.values():
            driver.volume_delete(volume=volume)

    @logwrap
    def volume_exists(self, volume):
        for driver in self.pool.values():
            if driver.volume_exists(volume=volume):
                return True

    @logwrap
    def volume_path(self, volume):
        ret = {}
        for control in self.pool.keys():
            ret[control] = self.pool[control].volume_path(volume=volume)
        return ret

    @logwrap
    def volume_upload(self, volume, path):
        for driver in self.pool.values():
            driver.volume_upload(volume, path)
