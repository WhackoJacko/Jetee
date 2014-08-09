__all__ = [u'project_configuration']


class LazyConfiguration(object):
    def __init__(self):
        self._configuration = None

    def _get_confuguration_class(self):
        from jetee.runtime.app import dispatcher

        configuration_module = __import__(dispatcher.args.configuration_module)
        project_configuration_class = getattr(configuration_module, dispatcher.args.configuration_name)
        return project_configuration_class

    def set_configuration(self, configuration_class):
        self._configuration = configuration_class()

    def __getattr__(self, item):
        if self._configuration is None:
            self.set_configuration(self._get_confuguration_class())
        return getattr(self._configuration, item)


project_configuration = LazyConfiguration()