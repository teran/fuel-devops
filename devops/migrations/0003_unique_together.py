# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Removing unique constraint on 'Network', fields ['environment', 'name']
        db.delete_unique(u'devops_network', ['environment_id', 'name'])

        # Removing unique constraint on 'Volume', fields ['environment', 'name']
        db.delete_unique(u'devops_volume', ['environment_id', 'name'])

        # Removing unique constraint on 'Node', fields ['environment', 'name']
        db.delete_unique(u'devops_node', ['environment_id', 'name'])

        # Adding unique constraint on 'Node', fields ['environment', 'node_control', 'name']
        db.create_unique(u'devops_node',
                         ['environment_id', 'node_control_id', 'name'])

        # Adding unique constraint on 'Volume', fields ['environment', 'node_control', 'name']
        db.create_unique(u'devops_volume',
                         ['environment_id', 'node_control_id', 'name'])

        # Adding unique constraint on 'Network', fields ['environment', 'node_control', 'name']
        db.create_unique(u'devops_network',
                         ['environment_id', 'node_control_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Network', fields ['environment', 'node_control', 'name']
        db.delete_unique(u'devops_network',
                         ['environment_id', 'node_control_id', 'name'])

        # Removing unique constraint on 'Volume', fields ['environment', 'node_control', 'name']
        db.delete_unique(u'devops_volume',
                         ['environment_id', 'node_control_id', 'name'])

        # Removing unique constraint on 'Node', fields ['environment', 'node_control', 'name']
        db.delete_unique(u'devops_node',
                         ['environment_id', 'node_control_id', 'name'])

        # Adding unique constraint on 'Node', fields ['environment', 'name']
        db.create_unique(u'devops_node', ['environment_id', 'name'])

        # Adding unique constraint on 'Volume', fields ['environment', 'name']
        db.create_unique(u'devops_volume', ['environment_id', 'name'])

        # Adding unique constraint on 'Network', fields ['environment', 'name']
        db.create_unique(u'devops_network', ['environment_id', 'name'])


    models = {
        u'devops.address': {
            'Meta': {'object_name': 'Address'},
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.related.ForeignKey', [],
                          {'to': u"orm['devops.Interface']"}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [],
                           {'max_length': '39'})
        },
        u'devops.diskdevice': {
            'Meta': {'object_name': 'DiskDevice'},
            'bus': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'device': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [],
                     {'to': u"orm['devops.Node']"}),
            'target_dev': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'type': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'volume': ('django.db.models.fields.related.ForeignKey', [],
                       {'to': u"orm['devops.Volume']", 'null': 'True'})
        },
        u'devops.environment': {
            'Meta': {'object_name': 'Environment'},
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [],
                     {'unique': 'True', 'max_length': '255'})
        },
        u'devops.interface': {
            'Meta': {'object_name': 'Interface'},
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [],
                            {'unique': 'True', 'max_length': '255'}),
            'model': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': u"orm['devops.Network']"}),
            'node': ('django.db.models.fields.related.ForeignKey', [],
                     {'to': u"orm['devops.Node']"}),
            'type': (
                'django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'devops.network': {
            'Meta': {
                'unique_together': "(('name', 'environment', 'node_control'),)",
                'object_name': 'Network'},
            'environment': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': u"orm['devops.Environment']",
                             'null': 'True'}),
            'forward': ('django.db.models.fields.CharField', [],
                        {'max_length': '255', 'null': 'True'}),
            'has_dhcp_server': (
                'django.db.models.fields.BooleanField', [], {}),
            'has_pxe_server': ('django.db.models.fields.BooleanField', [], {}),
            'has_reserved_ips': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'True'}),
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'ip_network': ('django.db.models.fields.CharField', [],
                           {'unique': 'True', 'max_length': '255'}),
            'name': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'node_control': ('django.db.models.fields.related.ForeignKey', [],
                             {'to': u"orm['devops.NodeControl']",
                              'null': 'True', 'blank': 'True'}),
            'tftp_root_dir': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'uuid': (
                'django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'devops.node': {
            'Meta': {
                'unique_together': "(('name', 'environment', 'node_control'),)",
                'object_name': 'Node'},
            'architecture': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'boot': ('django.db.models.fields.CharField', [],
                     {'default': "'[]'", 'max_length': '255'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': u"orm['devops.Environment']",
                             'null': 'True'}),
            'has_vnc': (
                'django.db.models.fields.BooleanField', [],
                {'default': 'True'}),
            'hypervisor': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'memory': (
                'django.db.models.fields.IntegerField', [],
                {'default': '1024'}),
            'metadata': ('django.db.models.fields.CharField', [],
                         {'max_length': '255', 'null': 'True'}),
            'name': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'node_control': ('django.db.models.fields.related.ForeignKey', [],
                             {'to': u"orm['devops.NodeControl']",
                              'null': 'True', 'blank': 'True'}),
            'os_type': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'role': ('django.db.models.fields.CharField', [],
                     {'max_length': '255', 'null': 'True'}),
            'uuid': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'vcpu': ('django.db.models.fields.PositiveSmallIntegerField', [],
                     {'default': '1'})
        },
        u'devops.nodecontrol': {
            'Meta': {'object_name': 'NodeControl'},
            'connection_string': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'node_controls'",
                             'to': u"orm['devops.Environment']"}),
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'name': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'pool': (
                'django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'devops.volume': {
            'Meta': {
                'unique_together': "(('name', 'environment', 'node_control'),)",
                'object_name': 'Volume'},
            'backing_store': ('django.db.models.fields.related.ForeignKey', [],
                              {'to': u"orm['devops.Volume']", 'null': 'True'}),
            'capacity': ('django.db.models.fields.BigIntegerField', [], {}),
            'environment': ('django.db.models.fields.related.ForeignKey', [],
                            {'to': u"orm['devops.Environment']",
                             'null': 'True'}),
            'format': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            u'id': (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True'}),
            'name': (
                'django.db.models.fields.CharField', [],
                {'max_length': '255'}),
            'node_control': ('django.db.models.fields.related.ForeignKey', [],
                             {'to': u"orm['devops.NodeControl']",
                              'null': 'True', 'blank': 'True'}),
            'uuid': (
                'django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['devops']