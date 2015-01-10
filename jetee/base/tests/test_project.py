from jetee.base.process import AbstractProcess
from jetee.base.project import AbstractProject
from jetee.base.config_factory import AnsibleTaskConfigFactory, AnsibleRoleConfigFactory


class TestAbstractProject(object):
    class FakeAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
        def get_config(self, **kwargs):
            return {u'fake': u'config'}

    class FakeAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
        def get_config(self, **kwargs):
            return {u'fake': u'config'}

    class FakeProject(AbstractProject):
        @property
        def deployment_config_factories(self):
            return [
                TestAbstractProject.FakeAnsibleTaskConfigFactory,
                TestAbstractProject.FakeAnsibleTaskConfigFactory,
                TestAbstractProject.FakeAnsibleRoleConfigFactory,
            ]

        @property
        def update_config_factories(self):
            return [
                TestAbstractProject.FakeAnsibleTaskConfigFactory,
                TestAbstractProject.FakeAnsibleRoleConfigFactory,
            ]

    def test_factory_deployment_confg_factories_list_of_configs(self):
        project = self.FakeProject(
            cvs_repo_url=u'git@github.com:WhackoJacko/Jetee.git',
            web_process=AbstractProcess()
        )
        config = project.factory_deployment_config()
        assert isinstance(config, list)
        assert len(config) == 3

    def test_factory_update_confg_factories_list_of_configs(self):
        project = self.FakeProject(
            cvs_repo_url=u'git@github.com:WhackoJacko/Jetee.git',
            web_process=AbstractProcess()
        )
        config = project.factory_update_config()
        assert isinstance(config, list)
        assert len(config) == 2