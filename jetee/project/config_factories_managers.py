from jetee.base.config_factories_manager import ConfigFactoriesManager
from jetee.common.config_factories.project.directories import ProjectDirectoriesAnsibleTaskConfigFactory
from jetee.common.config_factories.project.git import GITCloneAnsibleTaskConfigFactory
from jetee.common.config_factories.project.supervisor import SupervisorAnsibleRoleConfigFactory


class ProjectConfigFactoriesManager(ConfigFactoriesManager):
    initial_config_factories = (
        ProjectDirectoriesAnsibleTaskConfigFactory,
        GITCloneAnsibleTaskConfigFactory,
        SupervisorAnsibleRoleConfigFactory
    )