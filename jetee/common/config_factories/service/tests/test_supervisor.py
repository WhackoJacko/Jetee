from jetee.common.config_factories.service.supervisor import MakeSupervisorConfigForServiceAnsibleRoleConfigFactory
from jetee.base.project import AbstractProject


class TestMakeSupervisorConfigForServiceAnsibleRoleConfigFactory(object):
    def get_fake_service(self, FakeDockerService, FakeProcess):
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

    def test_config_rendered_properly(self, FakeDockerServiceClass, FakeProcessClass):
        config = MakeSupervisorConfigForServiceAnsibleRoleConfigFactory().get_config(
            self.get_fake_service(FakeDockerServiceClass, FakeProcessClass))[0]
        assert config[u'command'] == u'docker start -a test-name-fake-container'
        assert config[u'name'] == u'test-name-fake-container'
        assert config[u'process_name'] == u'test-name-fake-container'