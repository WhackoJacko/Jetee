from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory


class ElasticSearchService(DockerServiceAbstract):
    config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
    )

    image = u'dockerfile/elasticsearch'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=9200
        )
    ]