from jetee.base.project import ProjectAbstract
from jetee.common.config_factories.project.directories import ProjectDirectoriesAnsiblePreTaskConfigFactory
from jetee.common.config_factories.project.git import CloneGITRepoAnsiblePreTaskConfigFactory, \
    UpdateGITRepoAnsibleTaskConfigFactory
from jetee.common.config_factories.project.supervisor import SupervisorAnsibleRoleConfigFactory
from jetee.common.config_factories.project.supervisor import RestartSupervisorctlAnsibleRoleConfigFactory
from jetee.common.config_factories.project.pip import PIPRequirementsAnsibleTaskConfigFactory
from jetee.common.config_factories.project.apt import APTPackagesAnsibleTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoSyncdbAnsibleTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoMigrateAnsibleTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoCollectstaticAnsibleTaskConfigFactory


class DjangoProject(ProjectAbstract):
    deployment_config_factories_list = (
        ProjectDirectoriesAnsiblePreTaskConfigFactory,
        CloneGITRepoAnsiblePreTaskConfigFactory,
        APTPackagesAnsibleTaskConfigFactory,
        PIPRequirementsAnsibleTaskConfigFactory,
        DjangoSyncdbAnsibleTaskConfigFactory,
        DjangoMigrateAnsibleTaskConfigFactory,
        DjangoCollectstaticAnsibleTaskConfigFactory,
        SupervisorAnsibleRoleConfigFactory,
    )

    update_config_factories_list = (
        UpdateGITRepoAnsibleTaskConfigFactory,
        PIPRequirementsAnsibleTaskConfigFactory,
        DjangoSyncdbAnsibleTaskConfigFactory,
        DjangoMigrateAnsibleTaskConfigFactory,
        DjangoCollectstaticAnsibleTaskConfigFactory,
        RestartSupervisorctlAnsibleRoleConfigFactory,
    )

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(DJANGO_CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables


class PythonProject(ProjectAbstract):
    deployment_config_factories_list = (
        ProjectDirectoriesAnsiblePreTaskConfigFactory,
        CloneGITRepoAnsiblePreTaskConfigFactory,
        APTPackagesAnsibleTaskConfigFactory,
        PIPRequirementsAnsibleTaskConfigFactory,
        SupervisorAnsibleRoleConfigFactory,
    )

    update_config_factories_list = (
        UpdateGITRepoAnsibleTaskConfigFactory,
        PIPRequirementsAnsibleTaskConfigFactory,
        RestartSupervisorctlAnsibleRoleConfigFactory,
    )

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables