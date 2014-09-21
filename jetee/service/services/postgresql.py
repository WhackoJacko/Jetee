from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory


class PostgreSQLService(DockerServiceAbstract):
    config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
    )

    image = u'zumbrunnen/postgresql'
    command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=5432
        )
    ]