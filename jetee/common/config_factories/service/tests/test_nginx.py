from unittest import TestCase

from jetee.base.tests.base import FakeDockerService
from jetee.common.config_factories.service.nginx import NginxAnsibleRoleConfigFactory
from jetee.base.project import AbstractProject
from jetee.base.tests.base import FakeProcess


class NginxAnsibleRoleConfigFactoryTestCase(TestCase):
    def get_fake_service(self):
        return FakeDockerService(
            container_name=u'fake-container',
            volumes=[u'/usr/local/bin:/some/container/dir'],
            env_variables={u'ENV_VAR': u'ENV_VAR_VALUE'},
            project=AbstractProject(
                cvs_repo_url=u'git@github.com:WhackoJacko/Jetee.git',
                web_process=FakeProcess(
                )
            )
        )

    def test_config_factory_renders_valid_nginx_config(self):
        service = self.get_fake_service()
        config = NginxAnsibleRoleConfigFactory().get_config(parent=service)
        self.assertIn(u'test-name.fake-container', config[u'nginx_sites'])
        self.assertIn(u'server_name test-host.com', config[u'nginx_sites'][u'test-name.fake-container'])
        self.assertIn(
            u'location / { proxy_connect_timeout 300s; proxy_read_timeout 300s;proxy_pass http://unix:/var/jetee/test-name/sockets/fake-container.socket;}',
            config[u'nginx_sites'][u'test-name.fake-container']
        )
        self.assertIn(u'location /media/ {alias  /var/jetee/test-name/media/;}',
                      config[u'nginx_sites'][u'test-name.fake-container'])
        self.assertIn(u'location /static/ {alias  /var/jetee/test-name/static/;}',
                      config[u'nginx_sites'][u'test-name.fake-container'])