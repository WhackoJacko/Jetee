from jetee.service.deployers import DockerServiceDeployer


class AppConfiguration(object):
    hostname = u''
    username = u''
    server_names = []
    #
    project_name = None

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

    def get_project_name(self):
        if self.project_name:
            return self.project_name
        else:
            return u'.'.join(self.get_project().cvs_repo_url.split(u'/')[-1].split(u'.')[:-1])