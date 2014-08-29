from jetee.base.config_factory import AnsibleTaskConfigFactory


class ProjectDirectoriesAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
    _project_dir_template = {
        u'name': u'Ensure project directories exist',
        u'file': {
            u'path': u'',
            u'state': u'directory'
        }
    }

    def get_config(self, parent):
        project = parent

        project_dir_template = self._project_dir_template.copy()
        project_dir_template[u'file'][u'path'] = project.location

        return [project_dir_template, ]