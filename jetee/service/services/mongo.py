from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory


class MongoDBService(DockerServiceAbstract):
    """
    MongoDB service
    | Database name: docker
    | Username: docker
    | Password: docker
    """
    _config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
    )
    startup_priority = 3
    image = u'jetee/mongodb'
    # command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=27017
        )
    ]