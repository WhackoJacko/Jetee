from jetee.runtime.configuration import project_configuration
from jetee.base.config_factories_manager import ConfigManager


class PortsMapping(object):
    interface = u''
    external_port = u''
    internal_port = u''
    protocol = u''

    def __init__(self, internal_port=u'', interface=u'172.17.42.1', external_port=u'', protocol=u'tcp'):
        self.interface = interface
        self.external_port = external_port
        self.internal_port = internal_port
        self.protocol = protocol

    def get_representation(self):
        return u'{}:{}:{}/{}'.format(self.interface, self.external_port, self.internal_port, self.protocol)


class DockerServiceAbstract(object):
    config_factories_list = []
    config_manager_class = ConfigManager
    _container_name = None

    image = None
    hostname = None
    command = None
    ports_mappings = None
    volumes = None
    env_variables = None

    project = None

    def __init__(self, container_name=None, volumes=None, project=None, hostname=None, env_variables=None):
        self._container_name = container_name or self._container_name
        self.volumes = volumes or self.volumes
        self.project = project
        self.hostname = hostname or self.hostname
        self.ports_mappings = self.ports_mappings or []
        self.env_variables = env_variables or self.env_variables or {}

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
        return u'-'.join([project_configuration.get_project_name(), self.container_name])

    def factory_deployment_config(self):
        return self.config_manager_class(self, self.config_factories_list).factory()

    def set_project(self, project):
        self.project = project