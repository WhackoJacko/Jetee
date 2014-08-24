from jetee.base.common.config_factory import AnsibleTemplateMixin, AnsiblePreTaskConfigFactory


class PythonDependenciesAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    template = [
        {
            u'name': u'Install python dependencies',
            u'apt':
                {
                    u'name': u'{{item}}'
                },
            u'with_items': [
                u'python-setuptools', u'python-pip'
            ]
        }
    ]