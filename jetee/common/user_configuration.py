from jetee.service.deployers import DockerServiceDeployer


class AppConfiguration(object):
    HOSTNAME = u''
    USERNAME = u''
    SERVER_NAMES = []
    APT_PACKAGES = []
    TIMEZONE = u''
    #
    CVS_BRANCH = u''
    CVS_REPO_URL = u''

    PROJECT_NAME = None

    _main_service = None

    def get_service(self):
        """
        Template method to get main service, must return Service instance
        """
        raise NotImplementedError

    def get_project(self):
        """
        Template method to get app's project, must return Project instance
        """
        raise NotImplementedError

    def get_deployer(self):

        return DockerServiceDeployer()

    @property
    def main_service(self):
        if not self._main_service:
            self._main_service = self.get_service()
        return self._main_service

    @property
    def project_name(self):
        if self.PROJECT_NAME:
            return self.PROJECT_NAME
        else:
            return u'.'.join(self.CVS_REPO_URL.split(u'/')[-1].split(u'.')[:-1])