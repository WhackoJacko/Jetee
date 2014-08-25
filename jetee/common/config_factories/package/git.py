from jetee.base.config_factory import AnsibleTemplateMixin, AnsibleTaskConfigFactory


class GITPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsibleTaskConfigFactory):
    template = [
        {
            u'name': u'Install GIT package',
            u'apt':
                {
                    u'name': u'git'
                }
        }
    ]