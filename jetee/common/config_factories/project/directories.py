from jetee.base.config_factory import AnsibleTaskConfigFactory


class ProjectDirectoriesAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
    template = {
        u'name': u'Ensure project directories exist',
        u'file': {
            u'path': u'',
            u'state': u'directory'
        }
    }

    def get_config(self, parent):
        project = parent

        template = self.template.copy()
        template[u'file'][u'path'] = project.location

        return [template]