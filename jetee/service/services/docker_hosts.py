from jetee.base.service import AbstractDockerService, PortsMapping
from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory


class DockerHostsService(AbstractDockerService):
    startup_priority = 2
    image = u'jetee/docker-hosts'
    command = u'--domain-name=\'\' /srv/hosts'
    _config_factories_list = (
        DockerContainerAnsibleTaskConfigFactory,
        MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
    )
    _hosts_filename = u'/var/lib/docker/hosts'
    volumes = [
        u'/var/run/docker.sock:/var/run/docker.sock',
        u'{}:/srv/hosts'.format(_hosts_filename)
    ]

    @property
    def container_full_name(self):
        return u'docker-hosts'