from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory


class MongoDBService(DockerServiceAbstract):
    """
    MongoDB service
    | Database name: docker
    | Username: docker
    | Password: docker
    """
    _config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
    )

    image = u'dockerfile/mongodb'
    # command = u'/usr/bin/supervisord'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=27017
        )
    ]