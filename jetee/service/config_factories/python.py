from jetee.base.common.config_factory import AnsibleTemplatedTaskConfigFactory


class PythonDependenciesAnsibleConfigFactory(AnsibleTemplatedTaskConfigFactory):
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