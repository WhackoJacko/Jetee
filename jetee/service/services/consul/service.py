from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory
from .config_factories import ConsulNginxAnsibleRoleConfigFactory


class ConsulService(DockerServiceAbstract):
    image = u'jetee/consul'
    command = u'-server -bootstrap-expect 1'
    ports_mappings = [
        PortsMapping(internal_port=8500, external_port=8500),
        PortsMapping(internal_port=53, external_port=53, protocol=u'udp'),
    ]
    hostname = u'consul'
    config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
        ConsulNginxAnsibleRoleConfigFactory
    )

    @property
    def container_full_name(self):
        return u'consul'