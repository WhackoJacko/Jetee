import os

from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.runtime.configuration import project_configuration
from jetee.common.discoverer import ConsulDiscoverer
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory
from jetee.common.config_factories.service.nginx import NginxAnsibleRoleConfigFactory


class PrimaryService(DockerServiceAbstract):
    """
    Primary service
    """
    _container_name = u'project'
    _config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
        NginxAnsibleRoleConfigFactory,
    )

    image = u'jetee/blank'
    command = u'supervisord --nodaemon'
    volumes = [
        u'/root/.ssh/:/root/.ssh',
    ]
    ports_mappings = [
        PortsMapping(internal_port=22, interface=u'0.0.0.0'),  #for sshd
    ]

    def _get_container_port(self):
        server_name = u'{}.service.consul'.format(self.container_full_name)
        return ConsulDiscoverer().discover(server_name)