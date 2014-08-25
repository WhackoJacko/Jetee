#encoding=utf8
import os
import uuid

import yaml

from jetee.base.config import AnsibleTaskConfig, AnsibleRoleConfig


class AnsibleRoleConfigFactory(object):
    def get_config(self, **kwargs):
        return [kwargs]

    def factory(self, **kwargs):
        return AnsibleRoleConfig(config=self.get_config(**kwargs))


class AnsibleTaskConfigFactoryAbstract(object):
    variables = None
    _config_dir = u'/tmp/'
    task_type = None

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
            variables=self.variables,
            type=self.task_type
        )


class AnsibleTaskConfigFactory(AnsibleTaskConfigFactoryAbstract):
    task_type = AnsibleTaskConfig.TYPE_TASK


class AnsiblePreTaskConfigFactory(AnsibleTaskConfigFactory):
    task_type = AnsibleTaskConfig.TYPE_PRE_TASK


class AnsiblePostTaskConfigFactory(AnsibleTaskConfigFactory):
    task_type = AnsibleTaskConfig.TYPE_POST_TASK


class AnsibleTemplateMixin(object):
    template = {}

    def get_config(self):
        return self.template