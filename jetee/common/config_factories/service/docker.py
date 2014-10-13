import os

from jetee.common.utils import remove_special_characters
from jetee.base.config_factory import AnsiblePreTaskConfigFactory
from jetee.common.utils import render_env_variables
from jetee.common.config_factories.service.nginx import NginxAnsibleRoleConfigFactory


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
            u'hostname': None
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
            external_socket_dir_name = (u'/'.join(
                NginxAnsibleRoleConfigFactory.get_proxy_pass_for_service(service).split(u'/')[:-1])).rstrip(u'/')
            internal_socket_dir_name = (u'/'.join(service.project.socket_filename.split(u'/')[:-1])).rstrip(u'/')
            socket_mapping = u'%s:%s' % (
                external_socket_dir_name,
                internal_socket_dir_name
            )
            volumes.append(socket_mapping)

        return volumes

    def get_service_env_variables(self, service):
        env_variables = {
            u'SERVICE_NAME': service.container_full_name
        }
        env_variables.update(service.env_variables)
        return env_variables

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
        template[u'docker'][u'dns'] = u'172.17.42.1'
        template[u'docker'][u'hostname'] = service.hostname
        for ports_binding in service.ports_mappings:
            template[u'docker'][u'ports'].append(ports_binding.get_representation())
        template[u'docker'][u'expose'] = [u'{}/tcp'.format(ports_binding.internal_port) for ports_binding in
                                          service.ports_mappings]
        return [template]