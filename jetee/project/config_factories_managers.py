from jetee.base.common.config_factories_manager import ConfigFactoriesManager
from jetee.common.config_factories.project.directories import ProjectDirectoriesAnsibleTaskConfigFactory
from jetee.common.config_factories.project.git import GITCloneAnsibleTaskConfigFactory


class ProjectConfigFactoriesManager(ConfigFactoriesManager):
    initial_config_factories = (
        ProjectDirectoriesAnsibleTaskConfigFactory,
        GITCloneAnsibleTaskConfigFactory
    )