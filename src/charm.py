#!/usr/bin/env python3

import sys
sys.path.append('lib')

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import (
    ActiveStatus,
    MaintenanceStatus,
)

from interface_mysql_provides import MySQL

import logging

import yaml

logging.basicConfig(level=logging.DEBUG)


class MariaDbCharm(CharmBase):
    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self.state.set_default(isStarted=False)
        self.mysql = MySQL(self, 'mysql')

        # The latest version of the Operator Framework will raise an error
        # if you simply provided `self` as the second argument. It now requires
        # that you always explicitly declare the handler for the event.
        self.framework.observe(self.on.start,
                               self.on_start)
        self.framework.observe(self.on.stop,
                               self.on_stop)
        self.framework.observe(self.on.update_status,
                               self.on_update_status)
        self.framework.observe(self.on.config_changed,
                               self.on_config_changed)
        self.framework.observe(self.on.upgrade_charm,
                               self.on_upgrade_charm)
        self.framework.observe(self.on.leader_elected,
                               self.on_leader_elected)
        self.framework.observe(self.on.mysql_relation_joined,
                               self.on_mysql_relation_joined)
        self.framework.observe(self.on.mysql_relation_changed,
                               self.on_mysql_relation_changed)
        self.framework.observe(self.on.mysql_relation_departed,
                               self.on_mysql_relation_departed)
        self.framework.observe(self.on.mysql_relation_broken,
                               self.on_mysql_relation_broken)
        self.framework.observe(self.mysql.on.new_client,
                               self.on_new_client)

    def on_start(self, event):
        logging.info('START')
        self.model.unit.status = MaintenanceStatus('Configuring pod')
        podSpec = self.makePodSpec()
        if self.model.unit.is_leader():
            self.model.pod.set_spec(podSpec)
        self.state.isStarted = True
        self.state.podSpec = podSpec
        self.model.unit.status = ActiveStatus('ready')

    def on_stop(self, event):
        logging.info('STOP')
        self.state.isStarted = False

    def on_update_status(self, event):
        logging.info('UPDATE STATUS')

    def on_config_changed(self, event):
        logging.info('CONFIG CHANGED')
        podSpec = self.makePodSpec()
        if self.state.podSpec != podSpec:
            self.model.unit.status = MaintenanceStatus('Configuring pod')
            self.model.pod.set_spec(podSpec)
        self.model.unit.status = ActiveStatus('ready')

    def on_upgrade_charm(self, event):
        logging.info('UPGRADING')
        logging.info('UPGRADED')

    def on_leader_elected(self, event):
        logging.info('LEADER ELECTED')

    def on_mysql_relation_joined(self, event):
        logging.info('MYSQL RELATION JOINED')

    def on_mysql_relation_changed(self, event):
        logging.info('MYSQL RELATION CHANGED')

    def on_mysql_relation_departed(self, event):
        logging.info('MYSQL RELATION DEPARTED')

    def on_mysql_relation_broken(self, event):
        logging.info('MYSQL RELATION BROKEN')

    def on_new_client(self, event):
        logging.info('NEW CLIENT')
        if not self.state.isStarted:
            logging.info('NEW CLIENT DEFERRED')
            return event.defer()
        logging.info('NEW CLIENT SERVING')
        event.client.serve(database=self.model.config['database'],
                           host=event.client.ingress_address,
                           port=self.model.config['mysql_port'],
                           user=self.model.config['user'],
                           password=self.model.config['password'],
                           root_password=self.model.config['root_password'])

    def makePodSpec(self):
        logging.info('MAKING POD SPEC')
        if self.model.config['ha-mode']:
            with open("templates/spec_template_ha.yaml") as spec_file:
                podSpecTemplate = spec_file.read()
            dockerImage = self.model.config['ha-image']
        else:
            with open("templates/spec_template.yaml") as spec_file:
                podSpecTemplate = spec_file.read()
            dockerImage = self.model.config['image']

        data = {
            "name": self.model.app.name,
            "docker_image": dockerImage,
            "mysql_port": int(self.model.config['mysql_port']),
            "root_password": self.model.config['root_password'],
            "application_name": self.meta.name,
            "user": self.model.config['user'],
            "password": self.model.config['password'],
            "database": self.model.config['database'],
        }
        podSpec = podSpecTemplate % data
        podSpec = yaml.load(podSpec)
        return podSpec


if __name__ == "__main__":
    main(MariaDbCharm)
