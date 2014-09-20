from jetee.base.config_factory import AnsibleRoleConfigFactory, AnsibleTaskConfigFactory, AnsibleTemplateMixin


class RedisPackageAnsibleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, **kwargs):
        template = {
            u'role': u'DavidWittman.redis'
        }
        return [template]


class RedisPyPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsibleTaskConfigFactory):
    template = [
        {
            u'easy_install': {u'name': u'redis'}
        }
    ]