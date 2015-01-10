from jetee.base.tests.fixtures import *


def pytest_configure():
    fake_sys_argv()
    fake_configuration()
    fake_playbook_runner()