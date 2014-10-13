from jetee.base.deployment_manager import DeploymentManagerAbstract
from jetee.common.config_factories.os.python import PythonDependenciesAnsibleConfigFactory
from jetee.common.config_factories.project.ssh import GenerateSSHKeyAndPromptUserAnsibleTaskConfigFactory


class ProjectDeploymentManager(DeploymentManagerAbstract):
    default_config_factories = (
        PythonDependenciesAnsibleConfigFactory,
        GenerateSSHKeyAndPromptUserAnsibleTaskConfigFactory,
    )

    def deploy(self, project_configuration):
        configs = self.factory_default_configs() + \
                  project_configuration.get_primary_service().project.factory_deployment_config()
        return self._run_playbook(
            configs,
            username=project_configuration.username,
            password=None,
            hostname=project_configuration.hostname,
            port=project_configuration.get_primary_service()._get_container_port()
        )

    def update(self, project_configuration):
        configs = project_configuration.get_primary_service().project.factory_update_config()
        return self._run_playbook(
            configs,
            username=project_configuration.username,
            password=None,
            hostname=project_configuration.hostname,
            port=project_configuration.get_primary_service()._get_container_port()
        )