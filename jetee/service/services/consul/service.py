from jetee.base.service import AbstractDockerService, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
from .config_factories import ConsulNginxAnsibleRoleConfigFactory


class ConsulService(AbstractDockerService):
    startup_priority = 2
    image = u'jetee/consul'
    command = u'-server -bootstrap -advertise 172.17.42.1'
    ports_mappings = [
        PortsMapping(internal_port=8500, external_port=8500),
        PortsMapping(internal_port=53, external_port=53, protocol=u'udp'),
    ]
    _config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory,
        ConsulNginxAnsibleRoleConfigFactory
    )

    @property
    def container_full_name(self):
        return u'consul'