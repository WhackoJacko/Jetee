from jetee.base.common.config_factory import AnsibleTemplateMixin, AnsibleTaskConfigFactory


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