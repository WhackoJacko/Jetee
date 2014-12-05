from unittest import TestCase

from jetee.base.project import ProjectAbstract
from jetee.base.process import AbstractProcess
from jetee.base.config_factory import AnsibleTaskConfigFactory, AnsibleRoleConfigFactory


class ProjectAbstractTestCase(TestCase):
    class FakeAnsibleTaskConfigFactory(AnsibleTaskConfigFactory):
        def get_config(self, **kwargs):
            return {u'fake': u'config'}

    class FakeAnsibleRoleConfigFactory(AnsibleRoleConfigFactory):
        def get_config(self, **kwargs):
            return {u'fake': u'config'}


    class FakeProject(ProjectAbstract):
        @property
        def _deployment_config_factories_list(self):
            return [
                ProjectAbstractTestCase.FakeAnsibleTaskConfigFactory,
                ProjectAbstractTestCase.FakeAnsibleTaskConfigFactory,
                ProjectAbstractTestCase.FakeAnsibleRoleConfigFactory,
            ]

        @property
        def _update_config_factories_list(self):
            return [
                ProjectAbstractTestCase.FakeAnsibleTaskConfigFactory,
                ProjectAbstractTestCase.FakeAnsibleRoleConfigFactory,
            ]

    def test_factory_deployment_confg_factories_list_of_configs(self):
        project = self.FakeProject(
            cvs_repo_url=u'git@github.com:WhackoJacko/Jetee.git',
            web_process=AbstractProcess()
        )
        config = project.factory_deployment_config()
        self.assertIsInstance(config, list)
        self.assertEqual(len(config), 3)

    def test_factory_update_confg_factories_list_of_configs(self):
        project = self.FakeProject(
            cvs_repo_url=u'git@github.com:WhackoJacko/Jetee.git',
            web_process=AbstractProcess()
        )
        config = project.factory_update_config()
        self.assertIsInstance(config, list)
        self.assertEqual(len(config), 2)