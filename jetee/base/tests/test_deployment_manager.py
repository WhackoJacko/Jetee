from jetee.base.deployment_manager import AbstractDeploymentManager
from jetee.base.config import AnsibleTaskConfig


class TestDeploymentManagerAbstract(object):
    def test_assembles_configs_in_result_config(
            self,
            fake_ansible_task_config,
            fake_ansible_role_config_that_needs_merge,
            fake_ansible_role_config_that_doesnt_need_merge
    ):
        deployment_manager = AbstractDeploymentManager()
        configs = [
            fake_ansible_role_config_that_needs_merge,
            fake_ansible_role_config_that_doesnt_need_merge,
            fake_ansible_task_config,
        ]
        result_config = deployment_manager._factory_playbook_config(configs=configs)
        assert isinstance(result_config, AnsibleTaskConfig)

    def test_merges_configs_properly(self, fake_ansible_task_config):
        deployment_manager = AbstractDeploymentManager()
        configs = [fake_ansible_task_config, [], ]
        merged_configs = deployment_manager.merge_into_one_level_list(configs)
        assert isinstance(merged_configs, list)
        assert fake_ansible_task_config in merged_configs

    def test_factories_task_with_env_variables(self, fake_ansible_task_config):
        deployment_manager = AbstractDeploymentManager()
        task = deployment_manager._factory_task(fake_ansible_task_config)
        assert isinstance(task, dict)
        assert u'include' in task.keys()
        assert u'var' in task.keys()


class TestFakeDeploymentManager(object):
    def test_factories_default_configs(self, FakeDeploymentManagerClass):
        deployment_manager = FakeDeploymentManagerClass()
        default_configs = deployment_manager.factory_default_configs()
        assert isinstance(default_configs, list)
        assert len(default_configs) == len(FakeDeploymentManagerClass.default_config_factories)