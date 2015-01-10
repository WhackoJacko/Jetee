from jetee.base.config import AnsibleTaskConfig, AnsibleRoleConfig


class TestTaskConfig(object):
    def test_task_config_correctly_defines_type(self):
        pre_task_config = AnsibleTaskConfig(u'', type=AnsibleTaskConfig.TYPE_PRE_TASK)
        assert pre_task_config.is_pre_task()

        task_config = AnsibleTaskConfig(u'', type=AnsibleTaskConfig.TYPE_TASK)
        assert task_config.is_task()

        post_task_config = AnsibleTaskConfig(u'', type=AnsibleTaskConfig.TYPE_POST_TASK)
        assert post_task_config.is_post_task()

    def test_repe_works_well(self):
        str(AnsibleTaskConfig(u'', type=AnsibleTaskConfig.TYPE_TASK))


class TestRoleConfig(object):
    def test_repr_works_well(self):
        str(AnsibleRoleConfig(config={u'role': u'jetee'}, needs_merge=True))