from jetee.base.project import ProjectAbstract
from jetee.common.config_factories.project.directories import ProjectDirectoriesAnsibleTaskConfigFactory
from jetee.common.config_factories.project.git import GITCloneAnsibleTaskConfigFactory
from jetee.common.config_factories.project.supervisor import SupervisorAnsibleRoleConfigFactory
from jetee.common.config_factories.project.pip import PIPRequirementsAnsibleTaskConfigFactory
from jetee.common.config_factories.project.apt import APTPackagesAnsibleTaskConfigFactory


class DjangoProject(ProjectAbstract):
    deployment_config_factories_list = (
        ProjectDirectoriesAnsibleTaskConfigFactory,
        GITCloneAnsibleTaskConfigFactory,
        APTPackagesAnsibleTaskConfigFactory,
        PIPRequirementsAnsibleTaskConfigFactory,
        SupervisorAnsibleRoleConfigFactory,
    )

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(DJANGO_CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables