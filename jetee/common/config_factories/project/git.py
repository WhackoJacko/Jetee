import os

from jetee.base.common.config_factory import AnsibleTaskConfigFactory
from jetee.runtime.configuration import project_configuration


class GITCloneAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
    _template = {
        u'name': u'Clone project',
        u'git': {
            u'accept_hostkey': u'yes',
            u'dest': u'',
            u'repo': u'',
            u'version': u''
        }
    }

    def get_config(self, parent):
        project = parent
        template = self._template.copy()
        template[u'git'][u'dest'] = os.path.join(project.location, project_configuration.get_project_name())
        template[u'git'][u'repo'] = project.cvs_repo_url
        template[u'git'][u'version'] = project.cvs_repo_branch
        return [template]