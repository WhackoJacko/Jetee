from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory


class PostgreSQLService(DockerServiceAbstract):
    """
    Postgresql service
    | Database name: docker
    | Username: docker
    | Password: docker
    """
    _config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
    )

    image = u'jetee/postgresql'
    command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=5432
        )
    ]