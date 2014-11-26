from jetee.base.project import ProjectAbstract
from jetee.common.config_factories.project.directories import ProjectDirectoriesAnsiblePreTaskConfigFactory
from jetee.common.config_factories.project.git import CloneGitRepoAnsiblePreTaskConfigFactory, \
    UpdateGitRepoAnsibleTaskConfigFactory, CheckoutGitBranchAnsibleTaskConfigFactory
from jetee.common.config_factories.project.supervisor import ProcessSupervisorAnsibleRoleConfigFactory
from jetee.common.config_factories.project.supervisor import RestartSupervisorctlAnsiblePostTaskConfigFactory
from jetee.common.config_factories.project.pip import PipRequirementsAnsiblePreTaskConfigFactory
from jetee.common.config_factories.project.apt import InstallAptPackagesAnsiblePreTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoSyncdbAnsiblePostTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoMigrateAnsiblePostTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoCollectstaticAnsiblePostTaskConfigFactory
from jetee.common.config_factories.project.cron import CronPreTaskConfigFactory


class DjangoProject(ProjectAbstract):
    _deployment_config_factories_list = (
        ProjectDirectoriesAnsiblePreTaskConfigFactory,
        CloneGitRepoAnsiblePreTaskConfigFactory,
        InstallAptPackagesAnsiblePreTaskConfigFactory,
        PipRequirementsAnsiblePreTaskConfigFactory,
        DjangoSyncdbAnsiblePostTaskConfigFactory,
        DjangoMigrateAnsiblePostTaskConfigFactory,
        DjangoCollectstaticAnsiblePostTaskConfigFactory,
        CronPreTaskConfigFactory,
        ProcessSupervisorAnsibleRoleConfigFactory,
        RestartSupervisorctlAnsiblePostTaskConfigFactory,
    )

    _update_config_factories_list = (
        CheckoutGitBranchAnsibleTaskConfigFactory,
        UpdateGitRepoAnsibleTaskConfigFactory,
        InstallAptPackagesAnsiblePreTaskConfigFactory,
        PipRequirementsAnsiblePreTaskConfigFactory,
        DjangoSyncdbAnsiblePostTaskConfigFactory,
        DjangoMigrateAnsiblePostTaskConfigFactory,
        DjangoCollectstaticAnsiblePostTaskConfigFactory,
        RestartSupervisorctlAnsiblePostTaskConfigFactory,
    )

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(DJANGO_CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables


class PythonProject(ProjectAbstract):
    _deployment_config_factories_list = (
        ProjectDirectoriesAnsiblePreTaskConfigFactory,
        CloneGitRepoAnsiblePreTaskConfigFactory,
        InstallAptPackagesAnsiblePreTaskConfigFactory,
        PipRequirementsAnsiblePreTaskConfigFactory,
        CronPreTaskConfigFactory,
        ProcessSupervisorAnsibleRoleConfigFactory,
        RestartSupervisorctlAnsiblePostTaskConfigFactory,
    )

    _update_config_factories_list = (
        CheckoutGitBranchAnsibleTaskConfigFactory,
        UpdateGitRepoAnsibleTaskConfigFactory,
        InstallAptPackagesAnsiblePreTaskConfigFactory,
        PipRequirementsAnsiblePreTaskConfigFactory,
        RestartSupervisorctlAnsiblePostTaskConfigFactory,
    )

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables