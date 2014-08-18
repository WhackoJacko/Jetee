#encoding=utf8
import os
import uuid

import yaml

from jetee.base.common.config import AnsibleTaskConfig, AnsibleRoleConfig


class AnsibleRoleConfigFactory(object):
    roles_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), u'../../roles'))

    def get_config(self, **kwargs):
        return [kwargs]

    def factory(self, **kwargs):
        return AnsibleRoleConfig(config=self.get_config(**kwargs))


class AnsibleTaskConfigFactory(object):
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
        return AnsibleTaskConfig(
            filename=config_filename,
            variables=self.variables
        )


class AnsibleTemplatedTaskConfigFactory(AnsibleTaskConfigFactory):
    template = {}

    def get_config(self):
        return self.template