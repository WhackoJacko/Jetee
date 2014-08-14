from jetee.base.common.config_factory import AnsibleConfigFactory
from jetee.base.service.deployer import DeployerAbstract
from jetee.service.config_factories.docker import DockerPackageAnsibleConfigFactory, DockerPyPackageAnsibleConfigFactory
from jetee.service.config_factories.etcd import ETCDPackageAnsibleConfigFactory, ETCDCtlPackageAnsibleConfigFactory
from jetee.service.config_factories.nginx import NginxPackageAnsibleConfigFactory
from jetee.service.config_factories.python import PythonDependenciesAnsibleConfigFactory
from jetee.service.config_factories.go import GoPackageAnsibleConfigFactory
from jetee.runtime.ansible import PlaybookRunner
from jetee.runtime.configuration import project_configuration


class DockerServiceDeployer(DeployerAbstract):
    default_config_factories = [
        DockerPackageAnsibleConfigFactory,
        NginxPackageAnsibleConfigFactory,
        GoPackageAnsibleConfigFactory,
        PythonDependenciesAnsibleConfigFactory,
        DockerPyPackageAnsibleConfigFactory,
        ETCDPackageAnsibleConfigFactory,
        ETCDCtlPackageAnsibleConfigFactory
    ]

    def deploy(self, service):
        default_configs = self._factory_default_configs()
        services_configs = self._factory_services_configs(service)
        configs = default_configs + services_configs
        playbook_config = self._factory_playbook_config(configs=configs)
        res = PlaybookRunner.run(
            playbook_config=playbook_config,
            project_configuration=project_configuration
        )

    def _factory_task(self, config):
        task = {u'include': config.filename}
        if config.variables:
            task.update(config.variables)
        return task

    def _factory_playbook_config(self, configs):
        template = {
            u'hosts': u'*',
            u'remote_user': project_configuration.USERNAME,
            u'tasks': [self._factory_task(config) for config in configs]
        }
        config = AnsibleConfigFactory().factory(**template)
        return config

    def _factory_default_configs(self):
        factored_configs = []
        for config_factory in self.default_config_factories:
            factored_config = config_factory().factory()
            factored_configs.append(factored_config)
        return factored_configs

    def _factory_services_configs(self, service):
        def factory(current_service, factored_configs, processed_services):
            if not current_service.container_name in processed_services:
                for linked_service in current_service.linked_services:
                    factory(linked_service, factored_configs, processed_services)
                config = current_service.factory_config()
                factored_configs += config
                processed_services.append(current_service.container_name)
            return factored_configs

        factored_configs = factory(service, [], [])
        return factored_configs