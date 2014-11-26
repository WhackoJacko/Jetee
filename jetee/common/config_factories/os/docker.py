from jetee.base.config_factory import AnsibleTemplateMixin, AnsiblePreTaskConfigFactory


class DockerPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
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
                "name": "lxc-docker-1.3.0"
            },
            "name": "install docker"
        }
    ]


class DockerPyPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    template = [
        {
            u'pip':
                {
                    u'name': u'docker-py'
                }
        }
    ]