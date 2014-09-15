from jetee.base.project import ProjectAbstract
from jetee.common.config_factories.project.directories import ProjectDirectoriesAnsiblePreTaskConfigFactory
from jetee.common.config_factories.project.git import CloneGITRepoAnsiblePreTaskConfigFactory, \
    UpdateGITRepoAnsibleTaskConfigFactory
from jetee.common.config_factories.project.supervisor import SupervisorAnsibleRoleConfigFactory
from jetee.common.config_factories.project.supervisor import RestartSupervisorctlAnsiblePostTaskConfigFactory
from jetee.common.config_factories.project.pip import PIPRequirementsAnsiblePreTaskConfigFactory
from jetee.common.config_factories.project.apt import APTPackagesAnsiblePreTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoSyncdbAnsiblePostTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoMigrateAnsiblePostTaskConfigFactory
from jetee.common.config_factories.project.django import DjangoCollectstaticAnsiblePostTaskConfigFactory


class DjangoProject(ProjectAbstract):
    deployment_config_factories_list = (
        ProjectDirectoriesAnsiblePreTaskConfigFactory,
        CloneGITRepoAnsiblePreTaskConfigFactory,
        APTPackagesAnsiblePreTaskConfigFactory,
        PIPRequirementsAnsiblePreTaskConfigFactory,
        DjangoSyncdbAnsiblePostTaskConfigFactory,
        DjangoMigrateAnsiblePostTaskConfigFactory,
        DjangoCollectstaticAnsiblePostTaskConfigFactory,
        SupervisorAnsibleRoleConfigFactory,
        RestartSupervisorctlAnsiblePostTaskConfigFactory,
    )

    update_config_factories_list = (
        UpdateGITRepoAnsibleTaskConfigFactory,
        PIPRequirementsAnsiblePreTaskConfigFactory,
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
    deployment_config_factories_list = (
        ProjectDirectoriesAnsiblePreTaskConfigFactory,
        CloneGITRepoAnsiblePreTaskConfigFactory,
        APTPackagesAnsiblePreTaskConfigFactory,
        PIPRequirementsAnsiblePreTaskConfigFactory,
        SupervisorAnsibleRoleConfigFactory,
        RestartSupervisorctlAnsiblePostTaskConfigFactory,
    )

    update_config_factories_list = (
        UpdateGITRepoAnsibleTaskConfigFactory,
        PIPRequirementsAnsiblePreTaskConfigFactory,
        RestartSupervisorctlAnsiblePostTaskConfigFactory,
    )

    def get_env_variables(self):
        from jetee.runtime.app import dispatcher

        env_variables = self.env_variables.copy()
        env_variables.update(CONFIGURATION=dispatcher.args.configuration_name)
        return env_variables