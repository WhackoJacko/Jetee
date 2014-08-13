#encoding=utf8
import os
import uuid

import yaml

from jetee.base.config import AnsibleConfig


class AnsibleConfigFactory(object):
    variables = None
    _config_dir = u'/tmp/'

    def get_config(self, **kwargs):
        return [kwargs]

    def get_config_filename(self):
        filename = u'{}_{}'.format(self.__class__.__name__, uuid.uuid1().hex)
        return os.path.join(self._config_dir, filename)

    def factory(self, **kwargs):
        config = self.get_config(**kwargs)
        config_filename = self.get_config_filename()
        config_file_stream = file(name=config_filename, mode=u'w')
        yaml.safe_dump(data=config, stream=config_file_stream)
        config_file_stream.close()
        return AnsibleConfig(filename=config_filename, variables=self.variables)


class AnsibleTemplatedConfigFactory(AnsibleConfigFactory):
    template = {}

    def get_config(self):
        return self.template