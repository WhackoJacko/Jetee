from jetee.base.project import ProjectAbstract
from jetee.project.config_factories_managers import ProjectConfigFactoriesManager


class DjangoProject(ProjectAbstract):
    deployment_config_factories_manager_class = ProjectConfigFactoriesManager

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(DJANGO_CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables