from jetee.runtime.configuration import project_configuration
from jetee.base.config_factories_manager import ConfigManager
from jetee.service.deployment_managers import DockerServiceDeploymentManager


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
    deployment_manager_class = DockerServiceDeploymentManager
    config_factories_list = []
    config_manager_class = ConfigManager
    _container_name = None

    image = None
    command = None
    ports_mappings = None
    volumes = None

    project = None

    def __init__(self, container_name=None, volumes=None, project=None):
        self._container_name = container_name or self._container_name
        self.volumes = volumes or self.volumes
        self.project = project

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
        return u'.'.join([project_configuration.get_project_name(), self.container_name])

    def factory_deployment_config(self):
        return self.config_manager_class(self, self.config_factories_list).factory()

    def deploy(self):
        deployment_manager = self.deployment_manager_class()
        return deployment_manager.deploy(self)

    def set_project(self, project):
        self.project = project