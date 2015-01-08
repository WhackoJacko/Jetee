from jetee.base.config_factory import AnsiblePreTaskConfigFactory


class HostsFileExistsAnsiblePreTaskConfigFactory(AnsiblePreTaskConfigFactory):
    def get_config(self, **kwargs):
        from jetee.service.services.docker_hosts import DockerHostsService

        return [{
                    u'name': u'Ensure hosts file exists',
                    u'file': {
                        u'path': DockerHostsService._hosts_filename,
                        u'state': u'touch'
                    }
                }]