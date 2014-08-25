from jetee.base.config_factory import AnsibleTaskConfigFactory
from jetee.base.config import AnsibleRoleConfig, AnsibleTaskConfig
from jetee.runtime.configuration import project_configuration


class DeploymentManagerAbstract(object):
    default_config_factories = ()

    def _factory_task(self, config):
        task = {u'include': config.filename}
        if config.variables:
            task.update(config.variables)
        return task

    def _normalize_configs(self, configs):
        """
        Normalizes list of configs as list of dictionaries,
        some config factories factory list of configs instead of dict
        :param configs:
        :return:
        """
        configs_normalized = []
        for config in configs:
            if isinstance(config, (list, tuple)):
                configs_normalized += list(config)
            else:
                configs_normalized += [config]
        return configs_normalized

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
            u'roles': self._normalize_configs(
                [config.config for config in filter(lambda x: isinstance(x, AnsibleRoleConfig), configs)]
            ),
        }
        config = AnsibleTaskConfigFactory().factory(**template)
        return config

    def _factory_default_configs(self):
        factored_configs = []
        for config_factory in self.default_config_factories:
            factored_config = config_factory().factory()
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