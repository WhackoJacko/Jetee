import os

from jetee.base.config_factory import AnsibleRoleConfigFactory


class SupervisorAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, parent):
        service = parent
        config = []
        config_template = {
            u'role': u'nicholsn.supervisor',
            u'name': u'',
            u'command': u'',
            u'directory': u'',
            u'user': u'root'
        }
        for process in service.processes:
            tmp_config_template = config_template.copy()
            tmp_config_template[u'name'] = process.get_name()
            tmp_config_template[u'command'] = process.get_command()
            tmp_config_template[u'directory'] = process.get_working_directory()
            config.append(tmp_config_template)
        return config