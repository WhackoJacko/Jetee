from jetee.base.common.deployment_manager import DeploymentManagerAbstract
from jetee.common.config_factories.package.etcd import ETCDPackageAnsibleConfigFactory, ETCDCtlPackageAnsibleConfigFactory
from jetee.common.config_factories.package.docker import DockerPackageAnsibleConfigFactory, \
    DockerPyPackageAnsibleConfigFactory
from jetee.common.config_factories.package.python import PythonDependenciesAnsibleConfigFactory
from jetee.common.config_factories.package.go import GoPackageAnsibleConfigFactory


class DockerServiceDeploymentManager(DeploymentManagerAbstract):
    default_config_factories = (
        DockerPackageAnsibleConfigFactory,
        GoPackageAnsibleConfigFactory,
        PythonDependenciesAnsibleConfigFactory,
        DockerPyPackageAnsibleConfigFactory,
        ETCDPackageAnsibleConfigFactory,
        ETCDCtlPackageAnsibleConfigFactory
    )

    def _factory_deployment_configs(self, configurable):
        def factory(current_service, factored_configs, processed_services):
            if not current_service.container_name in processed_services:
                for linked_service in current_service.linked_services:
                    factory(linked_service, factored_configs, processed_services)
                config = current_service.factory_deployment_config()
                factored_configs += config
                processed_services.append(current_service.container_name)
            return factored_configs

        factored_configs = factory(configurable, [], [])
        return factored_configs

    def deploy(self, configurable):
        from jetee.runtime.configuration import project_configuration

        configs = self._factory_deployment_configs(configurable) + self._factory_default_configs()
        return self._run_playbook(
            configs,
            hostname=project_configuration.hostname,
            password=None,
            username=project_configuration.username,
            port=22
        )