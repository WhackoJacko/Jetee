import os

from jetee.base.config_factory import AnsibleRoleConfigFactory


class NginxPackageAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, parent):
        service = parent
        from jetee.runtime.configuration import project_configuration
        # TODO: represent options as list of strings
        config = {
            u'role': u'jdauphant.nginx',
            u'nginx_sites':
                {
                    project_configuration.get_project_name(): [
                        u'listen 8080',
                        u'server_name %s' % u' '.join(project_configuration.server_names),
                        u'proxy_connect_timeout 300s',
                        u'proxy_read_timeout 300s',
                        u'location / { '
                        u'proxy_connect_timeout 300s; '
                        u'proxy_read_timeout 300s;'
                        u'proxy_pass %s' % u'http://172.17.42.1:{{%s_result["ansible_facts"]["docker_containers"]'
                                           u'[0]["NetworkSettings"]["Ports"]["9000/tcp"][0]["HostPort"]}}; }' % service.container_name
                    ]
                }
            ,
            u'nginx_configs': {
                u'proxy': [
                    u'proxy_set_header X-Real-IP $remote_addr',
                    u'proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for',
                    u'proxy_set_header Host $http_host',
                    u'proxy_set_header X-NginX-Proxy true',
                ]
            },
            u'nginx_http_params': [
                u'types_hash_max_size 2048',
                u'types_hash_bucket_size 32'
            ]
        }

        return config