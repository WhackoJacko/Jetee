import os

from jetee.base.config_factory import AnsiblePreTaskConfigFactory
from jetee.runtime.configuration import project_configuration


class PipRequirementsAnsiblePreTaskConfigFactory(AnsiblePreTaskConfigFactory):
    template = {
        u'name': u'Install PIP requirements',
        u'pip': {
            u'chdir': u'',
            u'requirements': u'',
        }
    }

    def get_config(self, parent):
        project = parent
        template = self.template.copy()
        template[u'pip'][u'chdir'] = os.path.join(project.location, project_configuration.get_project_name())
        template[u'pip'][u'requirements'] = project.requirements_location
        return [template]