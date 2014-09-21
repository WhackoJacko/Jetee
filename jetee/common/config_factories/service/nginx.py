from jetee.base.config_factory import AnsibleRoleConfigFactory


class NginxAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
    service_upstream = u'/var/jetee/%s/sockets/%s.socket'
    config_needs_merge = True

    @classmethod
    def get_proxy_pass_for_service(cls, service):
        from jetee.runtime.configuration import project_configuration

        return cls.service_upstream % (project_configuration.get_project_name(), service.container_name)

    def get_static_config(self, service):
        from jetee.runtime.configuration import project_configuration

        if service.project:
            return u'location /static/ {alias  /var/jetee/%s/static/;}' % project_configuration.get_project_name()
        return u''

    def get_media_config(self, service):
        from jetee.runtime.configuration import project_configuration

        if service.project:
            return u'location /media/ {alias  /var/jetee/%s/media/;}' % project_configuration.get_project_name()
        return u''

    def get_config(self, parent):
        service = parent
        from jetee.runtime.configuration import project_configuration

        config_name = u'.'.join([project_configuration.get_project_name(), service.container_name])
        config = {
            u'role': u'jdauphant.nginx',
            u'nginx_sites':
                {
                    config_name: [
                        u'listen 80',
                        u'server_name %s' % u' '.join(project_configuration.server_names),
                        u'proxy_connect_timeout 300s',
                        u'proxy_read_timeout 300s',
                        u'location / { '
                        u'proxy_connect_timeout 300s; '
                        u'proxy_read_timeout 300s;'
                        u'proxy_pass http://unix:%s;}' % self.get_proxy_pass_for_service(service),
                        self.get_media_config(service),
                        self.get_static_config(service)
                    ],
                    u'redirect_www': [
                        u'server_name "~^www\.(.*)$"',
                        u'return 301 $scheme://$1$request_uri'
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