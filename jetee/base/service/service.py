from jetee.service.config_factories.docker import AnsibleDockerContainerTaskConfigFactory
from jetee.service.config_factories.etcd_register import AnsibleETCDRegisterContainerTaskConfigFactory
from jetee.runtime.configuration import project_configuration


class PortsMapping(object):
    interface = u''
    external_port = u''
    internal_port = u''

    def __init__(self, internal_port, interface=u'', external_port=u''):
        self.interface = interface
        self.external_port = external_port
        self.internal_port = internal_port

    def get_representation(self):
        return u'{}:{}:{}'.format(self.interface, self.external_port, self.internal_port)


class LinkableMixin(object):
    _linked_services = []

    def uses(self, *services):
        if not self._linked_services:
            self._linked_services = []
        self._linked_services += services

    @property
    def linked_services(self):
        return self._linked_services


class DockerServiceAbstract(LinkableMixin):
    _deployer_class = None
    _config_factories = [
        AnsibleDockerContainerTaskConfigFactory,
        AnsibleETCDRegisterContainerTaskConfigFactory
    ]
    _container_name = None

    image = None
    command = None
    ports_mappings = None
    volumes = None

    def __init__(self, container_name=None):
        if container_name:
            self._container_name = container_name

    @property
    def container_name(self):
        """

        Returns container name, if self._container_name is not defined container name would be last part of image name

        :return:
        """
        if self._container_name:
            return self._container_name
        else:
            return self.image.split(u'/').pop()

    @property
    def container_full_name(self):
        """

        Returns container full name of the form {project_name.container_name}

        :return:
        """
        return u'.'.join([project_configuration.project_name, self.container_name])

    def factory_config(self):
        return [config_factory().factory(service=self) for config_factory in self._config_factories]