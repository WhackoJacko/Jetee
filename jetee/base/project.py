from jetee.base.config_factories_manager import ConfigManager
from jetee.project.deployment_managers import ProjectDeploymentManager


class ProjectAbstract(object):
    deployment_manager_class = ProjectDeploymentManager
    config_manager_class = ConfigManager

    deployment_config_factories_list = []
    update_config_factories_list = []

    processes = None

    cvs_repo_url = None
    cvs_repo_branch = None
    location = None
    static_location = None

    def __init__(self, cvs_repo_url, cvs_repo_branch=u'master', location=u'/app/', media_location=u'/app/media',
                 static_location=u'/app/static', processes=None, env_variables=None, apt_packages=None):
        self.cvs_repo_url = cvs_repo_url
        self.cvs_repo_branch = cvs_repo_branch
        self.location = location
        self.media_location = media_location
        self.static_location = static_location
        self.processes = processes
        self.env_variables = env_variables or {}
        self.apt_packages = apt_packages or []
        assert self.processes, u'At least one process must be specified for project'

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(PROJECT_CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables

    def factory_deployment_config(self):
        return self.config_manager_class(self, self.deployment_config_factories_list).factory()

    def deploy(self):
        deployment_manager = self.deployment_manager_class()
        return deployment_manager.deploy(self)