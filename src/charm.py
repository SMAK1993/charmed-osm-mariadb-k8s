#!/usr/bin/env python3

import sys
sys.path.append('lib')  # noqa: E402

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import (
    ActiveStatus,
    BlockedStatus,
    MaintenanceStatus,
    UnknownStatus,
    WaitingStatus,
    ModelError,
)

from interface_mysql import MySQLClient

import logging
import subprocess

import yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class MariaDbCharm(CharmBase):
    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        
        self.state.set_default(is_started=False)
        
        # TODO: install hook will only be relevant as soon as LP: #1854635 will be fixed.
        # self.framework.observe(self.on.install, self)
        self.framework.observe(self.on.start, self)
        self.framework.observe(self.on.stop, self)
        self.framework.observe(self.on.config_changed, self)
        # self.framework.observe(self.on.db_relation_joined, self)
        # self.framework.observe(self.on.db_relation_changed, self)

    # def on_install(self, event):
    #     logger.info('Running on_install hook')
    #     self.model.unit.status = MaintenanceStatus('Running on_install hook')

    def on_start(self, event):
        logger.info('Running on_start hook')
        self.model.unit.status = MaintenanceStatus('Configuring pod')
        podSpec = self.make_pod_spec()
        self.model.pod.set_spec(podSpec)
        self.state.isStarted = True
        self.state.podSpec = podSpec
        self.model.unit.status = ActiveStatus('ready')

    def on_stop(self, event):
        logger.info('Running on_stop')

    def on_config_changed(self, event):
        logger.info('Running on_config_changed hook')
        podSpec = self.make_pod_spec()
        if self.state.podSpec != podSpec:
            self.model.unit.status = MaintenanceStatus('Configuring pod')
            self.model.pod.set_spec(podSpec)
        self.model.unit.status = ActiveStatus('ready')

    def make_pod_spec(self):
        podSpec = {
            'version': 2,
            'containers': [{
                'name': self.model.app.name,
                'image': self.model.config['image'],
                'ports': [{
                    'containerPort': int(self.model.config['mysql_port']),
                    'protocol': 'TCP',
                    'name': 'main',
                }],
                'config': {
                    'MARIADB_ROOT_PASSWORD': self.model.config['root_password'],
                    'MARIADB_USER': self.model.config['user'],
                    'MARIADB_PASSWORD': self.model.config['password'],
                    'MARIADB_DATABASE': self.model.config['database'],
                },
                'kubernetes': {
                    'readinessProbe': {
                        'tcpSocket': {
                            'port': int(self.model.config['mysql_port']),
                        },
                        'initialDelaySeconds': 10,
                        'periodSeconds': 10,
                        'timeoutSeconds': 5,
                        'successThreshold': 1,
                        'failureThreshold': 3,
                    },
                    'livenessProbe': {
                        'tcpSocket': {
                            'port': int(self.model.config['mysql_port']),
                        },
                        'initialDelaySeconds': 120,
                        'periodSeconds': 10,
                        'timeoutSeconds': 5,
                        'successThreshold': 1,
                        'failureThreshold': 3,
                    },
                }
            }]
        }
        return podSpec

if __name__ == "__main__":
    main(MariaDbCharm)
