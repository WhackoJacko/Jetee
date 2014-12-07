from jetee.base.service import AbstractDockerService, PortsMapping
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory


class PostgreSQLService(AbstractDockerService):
    """
    Postgresql service
    | Database name: docker
    | Username: docker
    | Password: docker
    """
    _config_factories_list = (
        DockerContainerAnsibleTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
    )
    startup_priority = 3
    image = u'jetee/postgresql'
    command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=5432
        )
    ]