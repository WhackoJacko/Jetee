from jetee.base.config_factory import AnsibleTemplateMixin, AnsiblePreTaskConfigFactory


class DNSUtilsPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    template = [
        {
            u'apt':
                {
                    u'name': u'dnsutils'
                }
        }
    ]