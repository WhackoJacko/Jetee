from jetee.common.utils import remove_special_characters

from jetee.base.config_factory import AnsiblePreTaskConfigFactory


class AnsibleDockerContainerTaskConfigFactory(AnsiblePreTaskConfigFactory):
    _template = {
        u'name': u'Run {name} container',
        u'register': u'{name}_result',
        u'docker': {
            u'command': None,
            u'image': None,
            u'name': None,
            u'ports': None,
            u'detach': True,
            u'links': []
        }
    }

    def _get_env_variables(self, service):
        from jetee.runtime.app import dispatcher

        env_variables = {
            u'PROJECT_CONFIGURATION': dispatcher.args.configuration_name
        }
        if service.env_variables:
            env_variables.update(service.env_variables)
        return env_variables

    def render_env_variables(self, service):
        env_variables = self._get_env_variables(service)
        rendered_env_variables = u','.join([u'{}={}'.format(key,value) for key,value in env_variables.items()])
        return rendered_env_variables

    def get_config(self, parent):
        service = parent
        container_template = self._template.copy()
        container_template[u'name'] = container_template[u'name'].format(name=service.container_name)
        container_template[u'register'] = container_template[u'register'].format(
            name=remove_special_characters(service.container_name)
        )
        container_template[u'docker'][u'image'] = service.image
        container_template[u'docker'][u'command'] = service.command
        container_template[u'docker'][u'name'] = service.container_full_name
        container_template[u'docker'][u'volumes'] = service.volumes or []
        container_template[u'docker'][u'env'] = self.render_env_variables(service)
        container_template[u'docker'][u'ports'] = []
        for ports_binding in service.ports_mappings:
            container_template[u'docker'][u'ports'].append(ports_binding.get_representation())
        container_template[u'docker'][u'links'] = [
            u'{}:{}'.format(linked_service.container_full_name, linked_service.container_name) for linked_service in
            service.linked_services
        ]
        container_template[u'docker'][u'expose'] = [u'{}/tcp'.format(ports_binding.internal_port) for ports_binding in
                                                    service.ports_mappings]
        return [container_template]