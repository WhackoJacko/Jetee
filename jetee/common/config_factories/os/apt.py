from jetee.base.config_factory import AnsibleTemplateMixin, AnsiblePreTaskConfigFactory


class UpdateAptCachePackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    template = [
        {
            u'name': u'Update apt cache',
            u'apt':
                {
                    u'update_cache': u'yes'
                }
        }
    ]