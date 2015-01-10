import sys
import pytest

from jetee.runtime.configuration import project_configuration
from jetee.common.user_configuration import AppConfiguration
from jetee.base.deployment_manager import AbstractDeploymentManager
from jetee.base.service import AbstractDockerService
from jetee.base.config_factory import AnsibleTemplateMixin, AnsibleTaskConfig, AnsibleRoleConfig
from jetee.base.process import AbstractProcess
from jetee.base.service import PortsMapping
from jetee.base.project import AbstractProject
from jetee.base.config_factory import AnsibleTaskConfigFactory, AnsibleRoleConfigFactory


@pytest.fixture
def fake_ansible_role_config_that_needs_merge():
    return AnsibleRoleConfig(config={u'role': u'test-with-merge'}, needs_merge=True)


@pytest.fixture
def fake_ansible_role_config_that_doesnt_need_merge():
    return AnsibleRoleConfig(config={u'role': u'test-without-merge'}, needs_merge=False)


@pytest.fixture
def fake_ansible_task_config():
    return AnsibleTaskConfig(filename=u'some-file.yml', variables={u'var': u'value'})


@pytest.fixture
def FakeDeploymentManagerClass():
    class Class(AbstractDeploymentManager):
        default_config_factories = [
            AnsibleTaskConfigFactory,
            AnsibleRoleConfigFactory
        ]

    return Class


@pytest.fixture
def FakeAnsibleTempleMixinClass():
    class Class(AnsibleTemplateMixin):
        template = {u'some-key': u'value'}

    return Class


@pytest.fixture
def FakeProcessClass():
    class Class(AbstractProcess):
        name = u'fake-process'
        command = u'fake-command'

        env_variables = {u'key': u'value'}

        def get_name(self):
            return self.name

        def get_command(self):
            return self.command

    return Class


@pytest.fixture
def FakeDockerServiceClass():
    class Class(AbstractDockerService):
        image = u'jetee/fake'
        ports_mappings = [
            PortsMapping(
                internal_port=1234,
                external_port=4321,
                protocol=u'tcp'
            )
        ]

        def _get_container_port(self):
            return 22

    return Class


def fake_sys_argv():
    sys.argv = ['jetee', 'build']


def fake_playbook_runner():
    from jetee.runtime import ansible

    def fake_run(cls, **kwargs):
        return kwargs

    ansible.PlaybookRunner.run = classmethod(fake_run)


@pytest.fixture
def fake_configuration():
    class FakeAppConfiguration(AppConfiguration):
        hostname = u'test-host.com'
        username = u'test-user'
        project_name = u'test-name'
        server_names = [u'test-host.com']

        def get_primary_service(self):
            return FakeDockerServiceClass()(
                project=AbstractProject(
                    cvs_repo_url=u'',
                    web_process=AbstractProcess()
                )
            )

    project_configuration.set_configuration(FakeAppConfiguration)
    return FakeAppConfiguration