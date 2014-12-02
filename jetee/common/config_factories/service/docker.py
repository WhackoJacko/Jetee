import os
import re

from jetee.common.utils import remove_special_characters
from jetee.base.config_factory import AnsiblePreTaskConfigFactory
from jetee.common.utils import render_env_variables
from jetee.common.config_factories.service.nginx import NginxAnsibleRoleConfigFactory


class AnsibleDockerContainerTaskConfigFactory(AnsiblePreTaskConfigFactory):
    run_template = {
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
    stop_template = {
        u'name': u'Shutdown {name} container',
        u'when': u'{name}_result.changed',
        u'docker': {
            u'name': None,
            u'image': None,
            u'state': u'stopped'
        }
    }

    def get_web_process_socket_mapping(self, service):
        external_socket_dir_name = (u'/'.join(
            NginxAnsibleRoleConfigFactory.get_proxy_pass_for_service(service).split(u'/')[:-1])).rstrip(u'/')
        internal_socket_dir_name = (u'/'.join(service.project.web_process.socket_filename.split(u'/')[:-1])).rstrip(
            u'/')
        socket_mapping = u'%s:%s' % (
            external_socket_dir_name,
            internal_socket_dir_name
        )
        return socket_mapping

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

            volumes += [self.get_web_process_socket_mapping(service)]
        return volumes

    def get_service_env_variables(self, service):
        env_variables = {
            u'SERVICE_NAME': service.container_full_name
        }
        env_variables.update(service.env_variables)
        return env_variables

    def underscore_container_name(self, container_name):
        return re.sub(r"[^\w\s]", '_', container_name)

    def get_config(self, parent):
        service = parent
        run_template = self.run_template.copy()
        run_template[u'name'] = run_template[u'name'].format(name=service.container_name)
        run_template[u'register'] = run_template[u'register'].format(
            name=self.underscore_container_name(service.container_name)
        )
        run_template[u'docker'][u'image'] = service.image
        run_template[u'docker'][u'command'] = service.command
        run_template[u'docker'][u'name'] = service.container_full_name
        run_template[u'docker'][u'volumes'] = self.get_container_volumes(service)
        run_template[u'docker'][u'ports'] = []
        run_template[u'docker'][u'dns'] = u'172.17.42.1'
        run_template[u'docker'][u'env'] = render_env_variables(self.get_service_env_variables(service))
        for ports_binding in service.ports_mappings:
            run_template[u'docker'][u'ports'].append(ports_binding.get_representation())
        run_template[u'docker'][u'expose'] = [u'{}/tcp'.format(ports_binding.internal_port) for ports_binding in
                                              service.ports_mappings]
        stop_template = self.stop_template.copy()
        stop_template[u'name'] = stop_template[u'name'].format(name=service.container_name)
        stop_template[u'when'] = stop_template[u'when'].format(
            name=self.underscore_container_name(service.container_name)
        )
        stop_template[u'docker'][u'name'] = service.container_full_name
        stop_template[u'docker'][u'image'] = service.image
        return [run_template, stop_template]