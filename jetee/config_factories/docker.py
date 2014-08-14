from jetee.utils import remove_special_characters

from jetee.base.config_factory import AnsibleTemplatedConfigFactory, AnsibleConfigFactory


class DockerPyPackageAnsibleConfigFactory(AnsibleTemplatedConfigFactory):
    template = [
        {
            u'pip':
                {
                    u'name': u'docker-py'
                }
        }
    ]


class DockerPackageAnsibleConfigFactory(AnsibleTemplatedConfigFactory):
    template = [
        {
            "apt_key": "url=\"https://get.docker.io/gpg\"",
            "name": "add docker repo key"
        },
        {
            "apt_repository": {
                "repo": "deb http://get.docker.io/ubuntu docker main",
                "update_cache": True
            },
            "name": "add docker repo server"
        },
        {
            "apt": {
                "name": "lxc-docker"
            },
            "name": "install docker"
        }
    ]


class AnsibleDockerContainerConfigFactory(AnsibleConfigFactory):
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

    def get_config(self, service):
        container_template = self._template.copy()
        container_template[u'name'] = container_template[u'name'].format(name=service.container_name)
        container_template[u'register'] = container_template[u'register'].format(
            name=remove_special_characters(service.container_name)
        )
        container_template[u'docker'][u'image'] = service.image
        container_template[u'docker'][u'command'] = service.command
        container_template[u'docker'][u'name'] = service.container_full_name
        container_template[u'docker'][u'volumes'] = service.volumes or []
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