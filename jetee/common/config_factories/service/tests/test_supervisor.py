from unittest import TestCase
from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
from jetee.base.tests.base import FakeDockerService, FakeProcess
from jetee.base.project import AbstractProject


class MakeSupervisorConfigForServiceAnsibleRoleConfigFactoryTestCase(TestCase):
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

    def test_config_rendered_properly(self):
        config = MakeSupervisorConfigForServiceAnsibleRoleConfigFactory().get_config(self.get_fake_service())[0]
        self.assertEqual(config[u'command'], u'docker start -a test-name-fake-container')
        self.assertEqual(config[u'name'], u'test-name-fake-container')
        self.assertEqual(config[u'process_name'], u'test-name-fake-container')
