from jetee.base.config_factory import AnsibleRoleConfigFactory


class ConsulNginxAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    config_needs_merge = True

    def get_config(self, parent):
        service = parent
        from jetee.runtime.configuration import project_configuration

        config_name = u'consul'
        config = {
            u'role': u'jdauphant.nginx',
            u'nginx_sites':
                {
                    config_name: [
                        u'listen 8501',
                        u'server_name %s' % u' '.join(project_configuration.server_names),
                        u'proxy_connect_timeout 300s',
                        u'proxy_read_timeout 300s',
                        u'location / { '
                        u'proxy_connect_timeout 300s; '
                        u'proxy_read_timeout 300s;'
                        u'proxy_pass http://172.17.42.1:8500; }',
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
            }
        }

        return config