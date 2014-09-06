from unittest import TestCase

from jetee.base import config_factory
from jetee.base.config import AnsibleRoleConfig, AnsibleTaskConfig


class TestAnsibleTaskConfigFactory(TestCase):
    def test_task_config_factory_factories_task_confg(self):
        config = config_factory.AnsibleTaskConfigFactory().factory()
        self.assertIsInstance(config, AnsibleTaskConfig)
        self.assertEqual(config.type, AnsibleTaskConfig.TYPE_TASK)

    def test_pretask_config_factory_factories_pretask_confg(self):
        config = config_factory.AnsiblePreTaskConfigFactory().factory()
        self.assertIsInstance(config, AnsibleTaskConfig)
        self.assertEqual(config.type, AnsibleTaskConfig.TYPE_PRE_TASK)

    def test_posttask_config_factory_factories_posttask_confg(self):
        config = config_factory.AnsiblePostTaskConfigFactory().factory()
        self.assertIsInstance(config, AnsibleTaskConfig)
        self.assertEqual(config.type, AnsibleTaskConfig.TYPE_POST_TASK)


class TestAnsibleRoleConfig(TestCase):
    def test_role_config_factory_factories_role_confg(self):
        config = config_factory.AnsibleRoleConfigFactory().factory()
        self.assertIsInstance(config, AnsibleRoleConfig)