from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory


class RedisService(DockerServiceAbstract):
    """
    Redis service
    """
    _config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
    )
    startup_priority = 2
    image = u'redis'
    command = u'redis-server'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=6379
        )
    ]