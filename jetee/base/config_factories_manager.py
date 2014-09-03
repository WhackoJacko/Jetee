class ConfigManager(object):
    _config_factories = []
    _parent = None

    def __init__(self, parent, config_factories_list):
        self._parent = parent
        self._config_factories = list(config_factories_list)

    def factory(self):
        return [config_factory().factory(parent=self._parent) for config_factory in self._config_factories]