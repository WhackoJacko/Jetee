import os

from jetee.base.config_factory import AnsibleTaskConfigFactory
from jetee.runtime.configuration import project_configuration


class APTPackagesAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
    template = {
        u'name': u'Install APT packages',
        u'action': u'apt pkg={{item}} state=installed',
        u'with_items': None

    }

    def get_config(self, parent):
        project = parent
        template = self.template.copy()
        template[u'with_items'] = list(project.apt_packages) + [u'nano']
        return [template]