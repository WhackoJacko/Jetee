from jetee.base.config_factory import AnsibleRoleConfigFactory, AnsibleTemplateMixin


class NginxPackageBootstrapAnsibleRoleConfigFactory(AnsibleTemplateMixin, AnsibleRoleConfigFactory):
    config_needs_merge = True

    template = {
        u'role': u'jdauphant.nginx',
        u'nginx_http_params': [
            u'types_hash_max_size 2048',
            u'types_hash_bucket_size 64',
            u'server_names_hash_bucket_size 64'
        ]
    }