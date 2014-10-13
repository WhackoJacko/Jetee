from jetee.base.service import DockerServiceAbstract
from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory


class RegistratorService(DockerServiceAbstract):
    image = u'jetee/registrator'
    command = u'consul://172.17.42.1:8500'
    volumes = [u'/var/run/docker.sock:/tmp/docker.sock']
    _config_factories_list = (
        AnsibleDockerContainerTaskConfigFactory,
    )

    @property
    def container_full_name(self):
        return self.container_name