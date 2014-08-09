from jetee.base.config_factory import AnsibleTemplatedConfigFactory


class NginxPackageAnsibleConfigFactory(AnsibleTemplatedConfigFactory):
    template = [
        {
            "apt": "pkg=nginx state=latest",
            "name": "ensure nginx is installed and at the latest version"
        },
        {
            "name": "ensure nginx is running",
            "service": "name=nginx state=started"
        }
    ]