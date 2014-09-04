import os

from jetee.base.config_factory import AnsibleTaskConfigFactory
from jetee.runtime.configuration import project_configuration

__all__ = [u'DjangoSyncdbAnsibleTaskConfigFactory', u'DjangoCollectstaticAnsibleTaskConfigFactory',
           u'DjangoMigrateAnsibleTaskConfigFactory']


class DjangoManagementAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
    template = {
    }

    def get_config(self, parent):
        project = parent
        template = self.template.copy()
        template[u'django_manage'][u'app_path'] = os.path.join(project.location,
                                                               project_configuration.get_project_name())
        if project.get_env_variables():
            template[u'environment'] = project.get_env_variables()
        return [template]


class DjangoSyncdbAnsibleTaskConfigFactory(DjangoManagementAnsibleTaskConfigFactory):
    template = {
        u'name': u'Syncdb',
        u'django_manage': {
            u'app_path': u'',
            u'command': u'syncdb',
        }
    }


class DjangoMigrateAnsibleTaskConfigFactory(DjangoManagementAnsibleTaskConfigFactory):
    template = {
        u'name': u'Migrate',
        u'django_manage': {
            u'app_path': u'',
            u'command': u'migrate',
        }
    }


class DjangoCollectstaticAnsibleTaskConfigFactory(DjangoManagementAnsibleTaskConfigFactory):
    template = {
        u'name': u'Collectstatic',
        u'django_manage': {
            u'app_path': u'',
            u'command': u'collectstatic',
        }
    }