from jetee.base.config_factory import AnsibleTemplatedConfigFactory


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