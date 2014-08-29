from jetee.base.exceptions import ImproperlyConfigured


class AppConfiguration(object):
    hostname = u''
    username = u''
    server_names = []
    #
    project_name = None

    _main_service = None

    def __init__(self):
        assert self.hostname, u'Hostname required'
        assert self.server_names, u'At least one server name required'
        assert self.username, u'Username required'

    def get_service(self):
        """
        Template method to get main service, must return Service instance
        """
        raise NotImplementedError

    def get_project_name(self):
        if self.project_name:
            return self.project_name
        elif self.get_service().project:
            return u'.'.join(self.get_service().project.cvs_repo_url.split(u'/')[-1].split(u'.')[:-1])
        else:
            raise ImproperlyConfigured(u'You must specify either project or project_name')