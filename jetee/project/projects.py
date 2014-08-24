from jetee.base.project.project import ProjectAbstract
from jetee.project.config_factories_managers import ProjectConfigFactoriesManager


class DjangoProject(ProjectAbstract):
    deployment_config_factories_manager_class = ProjectConfigFactoriesManager