import os

from jetee.base.config_factory import AnsibleRoleConfigFactory, AnsibleTaskConfigFactory
from jetee.base.config import AnsibleRoleConfig, AnsibleTaskConfig


class TestAnsibleRoleConfigFactory(object):
    def test_role_config_factory_factories_role_config(self):
        role_config = AnsibleRoleConfigFactory().factory(**{u'role': u'jetee', u'some': u'value'})
        assert isinstance(role_config, list)
        assert len(role_config) == 1
        assert isinstance(role_config[0], AnsibleRoleConfig)


class TestAnsibleTaskConfigFactory(object):
    def test_task_config_factory_factories_task_config(self):
        task_config = AnsibleTaskConfigFactory().factory(**{u'role': u'jetee', u'some': u'value'})
        assert isinstance(task_config, AnsibleTaskConfig)

    def test_factored_task_config_file_exists(self):
        task_config = AnsibleTaskConfigFactory().factory(**{u'role': u'jetee', u'some': u'value'})
        assert os.path.exists(task_config.filename)

    def test_repr_works_well(self):
        str(AnsibleTaskConfigFactory())


class TestAnsibleTemplateMixin(object):
    def test_template(self, FakeAnsibleTempleMixinClass):
        assert FakeAnsibleTempleMixinClass.template == FakeAnsibleTempleMixinClass().get_config()