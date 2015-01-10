import pytest

from .deployment_managers import ProjectDeploymentManager
from jetee.base.config import AnsibleTaskConfig


class TestProjectDeploymentManager(object):
    @pytest.mark.parametrize(u'function', [u'deploy', u'update'])
    def test_deploy_and_update(self, function):
        from jetee.runtime.configuration import project_configuration

        result = getattr(ProjectDeploymentManager(), function)(project_configuration)
        assert result[u'username'] == project_configuration.username
        assert result[u'password'] == None
        assert result[u'hostname'] == project_configuration.hostname
        assert result[u'port'] == 22
        assert isinstance(result[u'playbook_config'], AnsibleTaskConfig)