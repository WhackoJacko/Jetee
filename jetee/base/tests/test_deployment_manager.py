from jetee.base.deployment_manager import DeploymentManagerAbstract
from jetee.base.config import AnsibleTaskConfig, AnsibleRoleConfig
from jetee.base.tests.base import FakeAppTestCase


class DeploymentManagerAbstractTestCase(FakeAppTestCase):
    def test_deployment_manager_assembles_configs_in_result_config(self):
        deployment_manager = DeploymentManagerAbstract()
        configs = [
            AnsibleRoleConfig(config={u'role': u'test-with-merge'}, needs_merge=True),
            AnsibleRoleConfig(config={u'role': u'test-without-merge'}, needs_merge=False),
            AnsibleTaskConfig(filename=u'some-file.yml', variables={u'var': u'value'}),
            [AnsibleTaskConfig(filename=u'some-another-file.yml')],
        ]
        result_config = deployment_manager._factory_playbook_config(configs=configs)
        self.assertIsInstance(result_config, AnsibleTaskConfig)

    def test_deployment_manager_merges_configs_properly(self):
        deployment_manager = DeploymentManagerAbstract()
        task_config_1 = AnsibleTaskConfig(filename=u'some-file.yml', variables={u'var': u'value'})
        task_config_2 = AnsibleTaskConfig(filename=u'some-another-file.yml')
        configs = [task_config_1, [task_config_2], ]
        merged_configs = deployment_manager.merge_into_one_level_list(configs)
        self.assertIsInstance(merged_configs, list)
        self.assertIn(task_config_1, merged_configs)
        self.assertIn(task_config_2, merged_configs)

    def test_deployment_manager_factories_task_with_env_variables(self):
        deployment_manager = DeploymentManagerAbstract()
        task_config = AnsibleTaskConfig(filename=u'some-file.yml', variables={u'var': u'value'})
        task = deployment_manager._factory_task(task_config)
        self.assertIsInstance(task, dict)
        self.assertIn(u'include', task.keys())
        self.assertIn(u'var', task.keys())