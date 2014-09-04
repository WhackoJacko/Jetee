import os

from jetee.base.config_factory import AnsibleRoleConfigFactory, AnsibleTaskConfigFactory


class SupervisorAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, parent):
        project = parent
        config = []
        template = {
            u'role': u'nicholsn.supervisor',
            u'name': u'',
            u'command': u'',
            u'directory': u'',
            u'user': u'root',
            u'env_vars': u''
        }
        for process in project.processes:
            tmp_template = template.copy()
            tmp_template[u'name'] = process.get_name()
            tmp_template[u'command'] = process.get_command()
            tmp_template[u'directory'] = process.get_working_directory()
            tmp_template[u'env_vars'] = project.get_env_variables()
            config.append(tmp_template)
        return config


class RestartSupervisorctlAnsibleRoleConfigFactory(AnsibleTaskConfigFactory):
    def get_config(self, parent):
        project = parent
        config = []
        template = {
            u'supervisorctl': {
                u'name': u'',
                u'state': u'restarted'
            }
        }
        for process in project.processes:
            tmp_template = template.copy()
            tmp_template[u'name'] = process.get_name()
            config.append(tmp_template)
        return config