from unittest import TestCase

from jetee.common.config_factories.service.nginx import NginxAnsibleRoleConfigFactory
from jetee.base.project import AbstractProject


class TestNginxAnsibleRoleConfigFactory(object):
    def get_fake_service(self, FakeDockerServiceClass, FakeProcessClass):
        return FakeDockerServiceClass(
            container_name=u'fake-container',
            volumes=[u'/usr/local/bin:/some/container/dir'],
            env_variables={u'ENV_VAR': u'ENV_VAR_VALUE'},
            project=AbstractProject(
                cvs_repo_url=u'git@github.com:WhackoJacko/Jetee.git',
                web_process=FakeProcessClass()
            )
        )

    def test_config_factory_renders_valid_nginx_config(self, FakeDockerServiceClass, FakeProcessClass):
        service = self.get_fake_service(FakeDockerServiceClass, FakeProcessClass)
        config = NginxAnsibleRoleConfigFactory().get_config(parent=service)
        assert u'test-name.fake-container' in config[u'nginx_sites']
        assert u'server_name test-host.com' in config[u'nginx_sites'][u'test-name.fake-container']
        assert u'location / { proxy_connect_timeout 300s; proxy_read_timeout 300s;proxy_pass http://unix:/var/jetee/test-name/sockets/fake-container.socket;}' in \
               config[u'nginx_sites'][u'test-name.fake-container']
        assert u'location /media/ {alias  /var/jetee/test-name/media/;}' in config[u'nginx_sites'][
            u'test-name.fake-container']
        assert u'location /static/ {alias  /var/jetee/test-name/static/;}' in config[u'nginx_sites'][
            u'test-name.fake-container']