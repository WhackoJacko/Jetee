import sys
import os

__all__ = [u'project_configuration']


class LazyConfiguration(object):
    def __init__(self):
        self._configuration = None

    def _get_confuguration_class(self):
        from jetee.runtime.app import dispatcher

        sys.path.insert(0, os.getcwd())
        try:
            configuration_module = __import__(dispatcher.args.configuration_module)
        except ImportError, e:
            if e.message == u'No module named {}'.format(dispatcher.args.configuration_module):
                print(u'Configuration module "{}" not found, make sure it is in sys.path.'.format(
                    dispatcher.args.configuration_module))
                exit()
            raise
        try:
            project_configuration_class = getattr(configuration_module, dispatcher.args.configuration_name)
        except AttributeError:
            print(u'Cannot find configuration class "{}" in "{}" module.'.format(dispatcher.args.configuration_name,
                                                                                 dispatcher.args.configuration_module))
            exit()
        else:
            return project_configuration_class

    def set_configuration(self, configuration_class):
        self._configuration = configuration_class()

    def __getattr__(self, item):
        if self._configuration is None:
            self.set_configuration(self._get_confuguration_class())
        return getattr(self._configuration, item)


project_configuration = LazyConfiguration()