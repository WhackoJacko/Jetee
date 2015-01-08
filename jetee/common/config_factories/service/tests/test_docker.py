from unittest import TestCase

from jetee.base.tests.base import FakeDockerService
from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory
from jetee.base.project import AbstractProject
from jetee.base.tests.base import FakeProcess


class DockerContainerAnsibleTaskConfigFactoryTestCase(TestCase):
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

    def test_config_factory_renders_valid_run_config(self):
        service = self.get_fake_service()
        config = DockerContainerAnsibleTaskConfigFactory().get_config(parent=service)
        run_template, _ = config
        self.assertEqual(run_template[u'docker'][u'name'], u'test-name-fake-container')
        self.assertEqual(
            run_template[u'docker'][u'env'],
            u'SERVICE_NAME=test-name-fake-container,ENV_VAR=ENV_VAR_VALUE'
        )
        self.assertEqual(run_template[u'docker'][u'image'], u'jetee/fake')
        self.assertIn(u'/usr/local/bin:/some/container/dir', run_template[u'docker'][u'volumes'])
        self.assertEqual(run_template[u'register'], u'test_name_fake_container_result')

    def test_config_factory_renders_valid_stop_config(self):
        service = FakeDockerService(
            container_name=u'fake-container',
            volumes=[u'/usr/local/bin:/some/container/dir'],
            project=None,
            env_variables={u'ENV_VAR': u'ENV_VAR_VALUE'}
        )
        config = DockerContainerAnsibleTaskConfigFactory().get_config(parent=service)
        _, stop_config = config
        self.assertEqual(stop_config[u'docker'][u'name'], u'test-name-fake-container')
        self.assertEqual(stop_config[u'docker'][u'state'], u'stopped')
        self.assertEqual(stop_config[u'when'], u'test_name_fake_container_result.changed')