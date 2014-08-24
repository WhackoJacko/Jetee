from jetee.common.config_factories.service.docker import AnsibleDockerContainerTaskConfigFactory
from jetee.common.config_factories.service.etcd_register import AnsibleETCDRegisterContainerTaskConfigFactory
from jetee.base.common.config_factories_manager import ConfigFactoriesManager
from jetee.common.config_factories.service.nginx import NginxPackageAnsibleRoleConfigFactory


class DockerServiceConfigManager(ConfigFactoriesManager):
    initial_config_factories = (
        AnsibleDockerContainerTaskConfigFactory,
        AnsibleETCDRegisterContainerTaskConfigFactory
    )


class AppDockerServiceConfigManager(ConfigFactoriesManager):
    initial_config_factories = DockerServiceConfigManager.initial_config_factories + (
    NginxPackageAnsibleRoleConfigFactory,)