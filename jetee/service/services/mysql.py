from jetee.base.service import AbstractDockerService, PortsMapping
from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory


class MySQLService(AbstractDockerService):
    """
    Mysql service

    Database name: docker

    Username: docker

    Password: docker
    """
    _config_factories_list = (
        DockerContainerAnsibleTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
    )
    startup_priority = 3
    image = u'jetee/mysql'
    # command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=3306
        )
    ]
    env_variables = {
        u'MYSQL_ROOT_PASSWORD': u'docker',
        u'MYSQL_USER': u'docker',
        u'MYSQL_DATABASE': u'docker',
        u'MYSQL_PASSWORD': u'docker'
    }