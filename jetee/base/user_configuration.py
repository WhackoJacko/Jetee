class UserConfiguration(object):
    HOSTNAME = u''
    USERNAME = u''
    SERVER_NAMES = []
    APT_PACKAGES = []
    TIMEZONE = u''

    CVS_BRANCH = u''
    CVS_REPO_URL = u''

    PROJECT_NAME = None

    def get_project_service(self):
        """
        Template method to get main service, must return Service instance
        """
        raise NotImplementedError

    @property
    def main_service(self):
        if not self._main_service:
            self._main_service = self.get_project_service()
        return self._main_service

    def get_project_name(self):
        if self.PROJECT_NAME:
            return self.PROJECT_NAME
        else:
            return u'.'.join(self.CVS_REPO_URL.split(u'/')[-1].split(u'.')[:-1])


class MockUserConfiguration(UserConfiguration):
    def __getattribute__(self, item):
        raise Exception(u'Project config not loaded!')