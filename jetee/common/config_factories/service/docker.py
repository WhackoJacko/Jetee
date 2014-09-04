from jetee.common.utils import remove_special_characters

from jetee.base.config_factory import AnsiblePreTaskConfigFactory


class AnsibleDockerContainerTaskConfigFactory(AnsiblePreTaskConfigFactory):
    template = {
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

    def get_container_volumes(self, service):
        from jetee.runtime.configuration import project_configuration

        volumes = service.volumes[:] if service.volumes else []
        if service.project:
            if service.project.media_location:
                media_directory = u'/var/jetee/%s/media/:%s' % (
                    project_configuration.get_project_name(), service.project.media_location.rstrip(u'/'))
                volumes.append(media_directory)
            if service.project.static_location:
                static_directory = u'/var/jetee/%s/static/:%s' % (
                    project_configuration.get_project_name(), service.project.static_location.rstrip(u'/'))
                volumes.append(static_directory)
        return volumes

    def get_config(self, parent):
        service = parent
        template = self.template.copy()
        template[u'name'] = template[u'name'].format(name=service.container_name)
        template[u'register'] = template[u'register'].format(
            name=remove_special_characters(service.container_name)
        )
        template[u'docker'][u'image'] = service.image
        template[u'docker'][u'command'] = service.command
        template[u'docker'][u'name'] = service.container_full_name
        template[u'docker'][u'volumes'] = self.get_container_volumes(service)
        template[u'docker'][u'ports'] = []
        for ports_binding in service.ports_mappings:
            template[u'docker'][u'ports'].append(ports_binding.get_representation())
        template[u'docker'][u'links'] = [
            u'{}:{}'.format(linked_service.container_full_name, linked_service.container_name) for linked_service in
            service.linked_services
        ]
        template[u'docker'][u'expose'] = [u'{}/tcp'.format(ports_binding.internal_port) for ports_binding in
                                                    service.ports_mappings]
        return [template]