import os
from jetee.base.common.config_factory import AnsibleRoleConfigFactory


class NginxPackageAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    def get_config(self, service):
        from jetee.runtime.configuration import project_configuration
        # TODO: represent options as list of strings
        config = {
            u'role': os.path.join(self.roles_dir, u'jdauphant.nginx'),
            u'nginx_sites':
                {
                    project_configuration.project_name: [
                        u'listen 8080',
                        # u'server_name': u'%s' % u' '.join(project_configuration.SERVER_NAMES),
                        # u'proxy_connect_timeout': u'300s',
                        # u'proxy_read_timeout': u'300s',
                        # u'location1': {
                        #     u'proxy_connect_timeout': u'300s',
                        #     u'proxy_read_timeout': u'300s',
                        #     u'proxy_pass': u'http://172.17.42.1:%s_result["ansible_facts"]["docker_containers"]'
                        #                    u'[0]["NetworkSettings"]["Ports"]["9000/tcp"][0]["HostPort"]' % service.container_name
                        # },
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