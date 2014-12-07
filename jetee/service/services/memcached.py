from jetee.base.service import AbstractDockerService, PortsMapping
from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory


class MemcachedService(AbstractDockerService):
    """
    Memcached service
    | Database name: docker
    | Username: docker
    | Password: docker
    """
    _config_factories_list = (
        DockerContainerAnsibleTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
    )
    startup_priority = 3
    image = u'jetee/memcached'
    # command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=11211
        )
    ]