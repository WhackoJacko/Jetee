import os
import pytest

from jetee.base.process import AbstractProcess


class TestAbstractProcess(object):
    @pytest.mark.xfail(raises=NotImplementedError)
    def test_name(self):
        AbstractProcess().get_name()

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_command(self):
        AbstractProcess().get_command()


class TestFakeProcess(object):
    def test_get_working_directory_works_properly(self, fake_configuration, FakeProcessClass):
        expected_cwd = os.path.join(
            fake_configuration().get_primary_service().project.location,
            fake_configuration().project_name
        )
        assert expected_cwd == FakeProcessClass().get_working_directory()

    def test_name(self, FakeProcessClass):
        assert FakeProcessClass().get_name() == FakeProcessClass.name

    def test_command(self, FakeProcessClass):
        assert FakeProcessClass().get_command() == FakeProcessClass.command

    def test_get_env_variables(self, FakeProcessClass):
        assert FakeProcessClass().get_env_variables() == FakeProcessClass.env_variables