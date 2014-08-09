from jetee.base.config_factory import AnsibleDockerContainerConfigFactory
from jetee.config_factories.etcd_register import AnsibleETCDRegisterContainerConfigFactory
from jetee.runtime.configuration import project_configuration


class PortsMapping(object):
    host_ip = u''
    external_port = u''
    internal_port = u''

    def __init__(self, internal_port, host_ip=u'', external_port=u''):
        self.host_ip = host_ip
        self.external_port = external_port
        self.internal_port = internal_port

    def get_representation(self):
        return u'{}:{}:{}'.format(self.host_ip, self.external_port, self.internal_port)


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
    _config_factories = [AnsibleDockerContainerConfigFactory, AnsibleETCDRegisterContainerConfigFactory]
    _container_name = None

    image_name = None
    cmd = None
    ports_mappings = None

    def __init__(self, container_name=None):
        if container_name:
            self._container_name = container_name

    @property
    def container_name(self):
        """
        Returns container name, if self._container_name is not defined container name would be '{project_name.image_name}'

        :return:
        """
        if self._container_name:
            return self._container_name
        else:
            container_name = u'.'.join([project_configuration.get_project_name(), self.image_name.replace(u'/', u'_')])
            return container_name

    def factory_config(self):
        return [config_factory().factory(service=self) for config_factory in self._config_factories]


class ProjectDockerService(DockerServiceAbstract):
    image_name = u'whackojacko/blank'
    cmd = u'supervisord --nodaemon'
    ports_mappings = [
        PortsMapping(internal_port=22, host_ip=u'0.0.0.0'),  #for sshd
        PortsMapping(internal_port=9000, host_ip=u'172.17.42.1')  #for project itself
    ]