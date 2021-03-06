import os

from jetee.base.config_factory import AnsiblePreTaskConfigFactory
from jetee.runtime.configuration import project_configuration


class CloneGitRepoAnsiblePreTaskConfigFactory(AnsiblePreTaskConfigFactory):
    template = {
        u'name': u'Checkout project repo',
        u'git': {
            u'accept_hostkey': u'yes',
            u'dest': u'',
            u'repo': u'',
            u'version': u''
        }
    }

    def get_config(self, parent):
        project = parent
        template = self.template.copy()
        template[u'git'][u'dest'] = os.path.join(project.location, project_configuration.get_project_name())
        template[u'git'][u'repo'] = project.cvs_repo_url
        template[u'git'][u'version'] = project.cvs_repo_branch
        return [template]


class UpdateGitRepoAnsibleTaskConfigFactory(AnsiblePreTaskConfigFactory):
    template = {
        u'name': u'Update project repo',
        u'command': u'git pull origin {}',
        u'args': {
            u'chdir': u''
        }
    }

    def get_config(self, parent):
        project = parent
        template = self.template.copy()
        template[u'command'] = template[u'command'].format(project.cvs_repo_branch)
        template[u'args'][u'chdir'] = os.path.join(project.location, project_configuration.get_project_name())
        return [template]


class CheckoutGitBranchAnsibleTaskConfigFactory(AnsiblePreTaskConfigFactory):
    template = {
        u'name': u'Checkout branch',
        u'command': u'git checkout {}',
        u'args': {
            u'chdir': u''
        }
    }

    def get_config(self, parent):
        project = parent
        template = self.template.copy()
        template[u'command'] = template[u'command'].format(project.cvs_repo_branch)
        template[u'args'][u'chdir'] = os.path.join(project.location, project_configuration.get_project_name())
        return [template]