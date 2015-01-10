from jetee.base.config_factories_manager import ConfigManager
from jetee.base.config_factory import AnsibleTaskConfigFactory, AnsibleRoleConfigFactory


class TestConfigManager(object):
    def test_config_manager_manages_config_factories(self):
        config_manager = ConfigManager(
            parent=u'',  # this would be kwarg for regular task config
            config_factories_list=[
                AnsibleTaskConfigFactory,
                AnsibleRoleConfigFactory,
                AnsibleTaskConfigFactory
            ]
        )
        configs = config_manager.factory()
        assert isinstance(configs, list)