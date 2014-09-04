import os

from jetee.base.config_factory import AnsibleRoleConfigFactory


class SupervisorAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, parent):
        project = parent
        config = []
        config_template = {
            u'role': u'nicholsn.supervisor',
            u'name': u'',
            u'command': u'',
            u'directory': u'',
            u'user': u'root',
            u'env_vars': u''
        }
        for process in project.processes:
            tmp_config_template = config_template.copy()
            tmp_config_template[u'name'] = process.get_name()
            tmp_config_template[u'command'] = process.get_command()
            tmp_config_template[u'directory'] = process.get_working_directory()
            tmp_config_template[u'env_vars'] = project.get_env_variables()
            config.append(tmp_config_template)
        return config