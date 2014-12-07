import os
from unittest import TestCase

from jetee.base.config_factory import AnsibleRoleConfigFactory, AnsibleTaskConfigFactory
from jetee.base.config import AnsibleRoleConfig, AnsibleTaskConfig


class AnsibleRoleConfigFactoryTestCase(TestCase):
    def test_role_config_factory_factories_role_config(self):
        role_config = AnsibleRoleConfigFactory().factory(**{u'role': u'jetee', u'some': u'value'})
        self.assertIsInstance(role_config, list)
        self.assertEqual(len(role_config), 1)
        self.assertIsInstance(role_config[0], AnsibleRoleConfig)


class AnsibleTaskConfigFactoryTestCase(TestCase):
    def test_task_config_factory_factories_task_config(self):
        task_config = AnsibleTaskConfigFactory().factory(**{u'role': u'jetee', u'some': u'value'})
        self.assertIsInstance(task_config, AnsibleTaskConfig)

    def test_factored_task_config_file_exists(self):
        task_config = AnsibleTaskConfigFactory().factory(**{u'role': u'jetee', u'some': u'value'})
        self.assertTrue(os.path.exists(task_config.filename))

    def test_repr_works_well(self):
        str(AnsibleTaskConfigFactory())