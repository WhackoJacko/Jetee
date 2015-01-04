import os

from jetee.base.service import AbstractDockerService, PortsMapping
from jetee.common.discoverer import ServiceDiscoverer
from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
from jetee.common.config_factories.service.nginx import NginxAnsibleRoleConfigFactory


class PrimaryService(AbstractDockerService):
    """
    Primary service
    """
    _container_name = u'project'
    _config_factories_list = (
        DockerContainerAnsibleTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory,
        NginxAnsibleRoleConfigFactory,
    )
    startup_priority = 4
    image = u'jetee/blank'
    command = u'supervisord --nodaemon'
    volumes = [
        u'/root/.ssh/:/root/.ssh',
        u'/var/lib/docker/hosts:/etc/hosts',
    ]
    ports_mappings = [
        PortsMapping(internal_port=22, interface=u'0.0.0.0'),  # for sshd
    ]

    def _get_container_port(self):
        return ServiceDiscoverer(self.container_full_name).discover_port()