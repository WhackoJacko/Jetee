from jetee.common.config_factories.service.docker import DockerContainerAnsibleTaskConfigFactory
from jetee.base.project import AbstractProject


class DockerContainerAnsibleTaskConfigFactoryTestCase(object):
    def get_fake_service(self, FakeProcess, FakeDockerServiceClass):
        return FakeDockerServiceClass(
            container_name=u'fake-container',
            volumes=[u'/usr/local/bin:/some/container/dir'],
            env_variables={u'ENV_VAR': u'ENV_VAR_VALUE'},
            project=AbstractProject(
                cvs_repo_url=u'git@github.com:WhackoJacko/Jetee.git',
                web_process=FakeProcess(
                )
            )
        )

    def test_config_factory_renders_valid_run_config(self, FakeProcess,FakeDockerServiceClass):
        service = self.get_fake_service(FakeProcess,FakeDockerServiceClass)
        config = DockerContainerAnsibleTaskConfigFactory().get_config(parent=service)
        run_template, _ = config
        assert run_template[u'docker'][u'name'] == u'test-name-fake-container'
        assert run_template[u'docker'][u'env'] == u'SERVICE_NAME=test-name-fake-container,ENV_VAR=ENV_VAR_VALUE'

        assert run_template[u'docker'][u'image'] == u'jetee/fake'
        assert u'/usr/local/bin:/some/container/dir' in run_template[u'docker'][u'volumes']
        assert run_template[u'register'] == u'test_name_fake_container_result'

    def test_config_factory_renders_valid_stop_config(self, FakeDockerService):
        service = FakeDockerService(
            container_name=u'fake-container',
            volumes=[u'/usr/local/bin:/some/container/dir'],
            project=None,
            env_variables={u'ENV_VAR': u'ENV_VAR_VALUE'}
        )
        config = DockerContainerAnsibleTaskConfigFactory().get_config(parent=service)
        _, stop_config = config
        assert stop_config[u'docker'][u'name'] == u'test-name-fake-container'
        assert stop_config[u'docker'][u'state'] == u'stopped'
        assert stop_config[u'when'] == u'test_name_fake_container_result.changed'