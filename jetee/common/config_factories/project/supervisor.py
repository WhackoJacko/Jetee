from jetee.base.config_factory import AnsibleRoleConfigFactory, AnsiblePostTaskConfigFactory
import copy


class ProcessSupervisorAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, parent):
        project = parent
        config = []
        template = {
            u'role': u'EDITD.supervisor_task',
            u'name': u'',
            u'command': u'',
            u'directory': u'',
            u'user': u'root',
            u'env_vars': u''
        }
        processes = [project.web_process] + project.helper_processes[:]
        for process in processes:
            tmp_template = template.copy()
            tmp_template[u'name'] = process.get_name()
            tmp_template[u'process_name'] = process.get_name()
            tmp_template[u'command'] = process.get_command()
            tmp_template[u'directory'] = process.get_working_directory()
            env_variables = project.get_env_variables()
            env_variables.update(process.get_env_variables())
            tmp_template[u'env_vars'] = env_variables
            config.append(tmp_template)
        return config


class RestartSupervisorctlAnsiblePostTaskConfigFactory(AnsiblePostTaskConfigFactory):
    def get_config(self, parent):
        project = parent
        config = []
        template = {
            u'name': u'Supervisor restart',
            u'supervisorctl': {
                u'name': u'',
                u'state': u'restarted'
            }
        }
        processes = [project.web_process] + project.helper_processes[:]
        for process in processes:
            tmp_template = copy.deepcopy(template)
            tmp_template[u'supervisorctl'][u'name'] = process.get_name()
            config.append(tmp_template)
        return config