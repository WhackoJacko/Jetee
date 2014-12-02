from jetee.base.config_factory import AnsibleRoleConfigFactory


class MakeSupervisorConfigForServiceAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, parent):
        service = parent
        template = {
            u'role': u'EDITD.supervisor_task',
            u'name': u'',
            u'command': u'',
            u'user': u'root',
            u'priority': 0,
            u'directory': u'/root/'
        }
        template = template.copy()
        template[u'name'] = service.container_full_name
        template[u'process_name'] = service.container_full_name
        template[u'command'] = u'docker start -a {}'.format(service.container_full_name)
        template[u'priority'] = service.startup_priority
        return [template]