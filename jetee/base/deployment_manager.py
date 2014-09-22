import uuid
from jetee.base.config_factory import AnsibleTaskConfigFactory
from jetee.base.config import AnsibleRoleConfig, AnsibleTaskConfig
from jetee.runtime.configuration import project_configuration
from jetee.common.utils import deep_merge


class DeploymentManagerAbstract(object):
    default_config_factories = ()


    def _factory_task(self, config):
        task = {u'include': config.filename}
        if config.variables:
            task.update(config.variables)
        return task

    def _normalize_role_configs(self, role_configs):
        """
        Normalizes roles configs so they wouldnt contain duplicated roles
        :param configs:
        :return:
        """

        def merge_into_one_level_list(items):
            merged_items = []
            for item in items:
                if isinstance(item.config, (list, tuple)):
                    merged_items += merge_into_one_level_list(item)
                else:
                    merged_items += [item]
            return merged_items

        merged_role_configs = merge_into_one_level_list(role_configs)
        normalized_configs = {}
        for role_config in merged_role_configs:
            if not role_config.config[u'role'] in normalized_configs.keys():
                if role_config.needs_merge:
                    configs_for_this_role = [
                        x.config for x in
                        filter(lambda x: x.config[u'role'] == role_config.config[u'role'], merged_role_configs)
                    ]
                    normalized_config = reduce(deep_merge, configs_for_this_role)
                    normalized_configs[role_config.config[u'role']] = normalized_config
                else:
                    normalized_configs[uuid.uuid1().get_hex()] = role_config.config[u'role']
        return normalized_configs.values()

    def _factory_playbook_config(self, configs):
        template = {
            u'hosts': u'*',
            u'remote_user': project_configuration.username,
            u'pre_tasks': [self._factory_task(config) for config in
                           filter(lambda x: isinstance(x, AnsibleTaskConfig) and x.is_pre_task(), configs)],
            u'tasks': [self._factory_task(config) for config in
                       filter(lambda x: isinstance(x, AnsibleTaskConfig) and x.is_task(), configs)],
            u'post_tasks': [self._factory_task(config) for config in
                            filter(lambda x: isinstance(x, AnsibleTaskConfig) and x.is_post_task(), configs)],
            u'roles': self._normalize_role_configs(filter(lambda x: isinstance(x, AnsibleRoleConfig), configs)
            ),
        }
        config = AnsibleTaskConfigFactory().factory(**template)
        return config

    def factory_default_configs(self):
        factored_configs = []
        for config_factory in self.default_config_factories:
            try:
                factored_config = config_factory().factory()
            except:
                import pdb;

                pdb.set_trace()
            factored_configs.append(factored_config)
        return factored_configs

    def _run_playbook(self, configs, hostname, port, username, password):

        from jetee.runtime.ansible import PlaybookRunner

        playbook_config = self._factory_playbook_config(configs=configs)
        res = PlaybookRunner.run(
            playbook_config=playbook_config,
            hostname=hostname,
            port=port,
            username=username,
            password=password
        )