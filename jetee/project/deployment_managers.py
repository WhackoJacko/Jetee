from jetee.base.deployment_manager import DeploymentManagerAbstract
from jetee.common.config_factories.package.python import PythonDependenciesAnsibleConfigFactory


class ProjectDeploymentManager(DeploymentManagerAbstract):
    default_config_factories = (
        PythonDependenciesAnsibleConfigFactory,
    )

    def deploy(self, configurable):
        from jetee.runtime.configuration import project_configuration

        configs = self._factory_default_configs() + configurable.factory_deployment_config()
        return self._run_playbook(
            configs,
            username=project_configuration.username,
            password=None,
            hostname=project_configuration.hostname,
            port=project_configuration.get_service().get_container_port()
        )