from jetee.base.config_factories_manager import ConfigManager
from jetee.project.deployment_managers import ProjectDeploymentManager


class ProjectAbstract(object):
    _deployment_manager_class = ProjectDeploymentManager
    _config_manager_class = ConfigManager

    _deployment_config_factories_list = []
    _update_config_factories_list = []

    web_process = None
    helper_processes = None

    cvs_repo_url = None
    cvs_repo_branch = None
    location = None
    static_location = None

    def __init__(self, cvs_repo_url, web_process=None, helper_processes=None, cvs_repo_branch=u'master',
                 location=u'/app/', media_location=u'/app/media', static_location=u'/app/static', env_variables=None,
                 apt_packages=None):
        self.cvs_repo_url = cvs_repo_url
        self.cvs_repo_branch = cvs_repo_branch
        self.location = location
        self.media_location = media_location
        self.static_location = static_location
        self.helper_processes = helper_processes or []
        self.web_process = web_process
        self.env_variables = env_variables or {}
        self.apt_packages = apt_packages or []
        assert (self.web_process or self.helper_processes), u'At least one process must be specified for project'

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(PROJECT_CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables

    def factory_deployment_config(self):
        return self._config_manager_class(self, self._deployment_config_factories_list).factory()

    def factory_update_config(self):
        return self._config_manager_class(self, self._update_config_factories_list).factory()

    def deploy(self):
        deployment_manager = self._deployment_manager_class()
        return deployment_manager.deploy(self)

    def update(self):
        deployment_manager = self._deployment_manager_class()
        return deployment_manager.update(self)