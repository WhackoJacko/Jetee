#encoding=utf8
import yaml
import os
import uuid

from jetee.base.config import AnsibleConfig


class AnsibleConfigFactory(object):
    variables = None
    _config_dir = u'/tmp/'

    def get_config(self, **kwargs):
        return [kwargs]

    def get_config_filename(self):
        filename = u'{}_{}'.format(self.__class__.__name__, uuid.uuid1().hex)
        return os.path.join(self._config_dir, filename)

    def factory(self, **kwargs):
        config = self.get_config(**kwargs)
        config_filename = self.get_config_filename()
        config_file_stream = file(name=config_filename, mode=u'w')
        yaml.safe_dump(data=config, stream=config_file_stream)
        config_file_stream.close()
        return AnsibleConfig(filename=config_filename, variables=self.variables)


class AnsibleTemplatedConfigFactory(AnsibleConfigFactory):
    template = {}

    def get_config(self):
        return self.template


class AnsibleDockerContainerConfigFactory(AnsibleConfigFactory):
    _template = {
        u'name': u'Run {name} container',
        u'register': u'{name}_result',
        u'docker': {
            u'image': None,
            u'name': None,
            u'ports': None,
            u'detach': True,
            u'links': []
        }
    }

    def get_config(self, service):
        container_template = self._template.copy()
        container_template[u'name'] = container_template[u'name'].format(name=service.container_name)
        container_template[u'register'] = container_template[u'register'].format(name=service.container_name)
        container_template[u'docker'][u'image'] = service.image_name
        container_template[u'docker'][u'name'] = service.container_name
        container_template[u'docker'][u'ports'] = []
        for ports_binding in service.ports_mappings:
            container_template[u'docker'][u'ports'].append(ports_binding.get_representation())
        container_template[u'docker'][u'links'] = [
            linked_service.container_name for linked_service in service.linked_services
        ]
        return [container_template]

