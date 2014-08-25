from jetee.base.config_factory import AnsibleTaskConfigFactory


class ProjectDirectoriesAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
    _project_dir_template = {
        u'name': u'Ensure project directories exist',
        u'file': {
            u'path': u'',
            u'state': u'directory'
        }
    }

    _media_dir_template = {
        u'name': u'Ensure media directory exists',
        u'file': {
            u'path': u'',
            u'state': u'directory'
        }
    }

    _static_dir_template = {
        u'name': u'Ensure static directory exists',
        u'file': {
            u'path': u'',
            u'state': u'directory'
        }
    }

    def get_config(self, parent):
        project = parent

        project_dir_template = self._project_dir_template.copy()
        project_dir_template[u'file'][u'path'] = project.location

        media_dir_template = self._media_dir_template.copy()
        media_dir_template[u'file'][u'path'] = project.media_location

        static_dir_template = self._static_dir_template.copy()
        static_dir_template[u'file'][u'path'] = project.static_location

        return [project_dir_template, media_dir_template, static_dir_template]