class ConfigFactoriesManager(object):
    initial_config_factories = ()
    _config_factories = []
    _parent = None

    def __init__(self, parent):
        self._parent = parent
        self._config_factories = list(self.initial_config_factories)

    def factory(self):
        return [config_factory().factory(parent=self._parent) for config_factory in self._config_factories]