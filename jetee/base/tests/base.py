import sys
from unittest import TestCase

from jetee.runtime.configuration import project_configuration
from jetee.common.user_configuration import AppConfiguration


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