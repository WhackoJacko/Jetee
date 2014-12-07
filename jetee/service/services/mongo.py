from jetee.base.service import AbstractDockerService, PortsMapping
from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory


class MongoDBService(AbstractDockerService):
    """
    MongoDB service
    """
    _config_factories_list = (
        DockerContainerAnsibleTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
    )
    startup_priority = 3
    image = u'jetee/mongodb'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=27017
        )
    ]