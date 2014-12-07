import sys
from unittest import TestCase

from jetee.runtime.configuration import project_configuration
from jetee.common.user_configuration import AppConfiguration
from jetee.base.service import AbstractDockerService
from jetee.base.process import AbstractProcess
from jetee.base.service import PortsMapping


class FakeProcess(AbstractProcess):
    def get_name(self):
        return u'fake-process'

    def get_command(self):
        return u'fake-command'


class FakeDockerService(AbstractDockerService):
    image = u'jetee/fake'
    ports_mappings = [
        PortsMapping(
            internal_port=1234,
            external_port=4321,
            protocol=u'tcp'
        )
    ]


class FakeAppTestCase(TestCase):
    def fake_sys_argv(self):
        sys.argv = ['jetee', 'build']

    def fake_configuration(self):
        class FakeAppConfiguration(AppConfiguration):
            hostname = u'test-host.com'
            username = u'test-user'
            project_name = u'test-name'
            server_names = [u'test-host.com']

        project_configuration.set_configuration(FakeAppConfiguration)

    def setUp(self):
        self.fake_sys_argv()
        self.fake_configuration()