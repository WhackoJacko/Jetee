import sys
from unittest.case import TestCase

from jetee.runtime.configuration import project_configuration
from jetee.base.user_configuration import UserConfiguration
from jetee.base.service.docker import ProjectDockerService, DockerServiceAbstract, PortsMapping
from jetee.base.deployers.docker import DockerServiceDeployer


class DockerDeployerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        sys.argv = [u'create',]
        class AppConfiguration(UserConfiguration):
            HOSTNAME = u'example.ru'
            USERNAME = u'root'
            SERVER_NAMES = [HOSTNAME]
            CVS_BRANCH = u'master'
            CVS_REPO_URL = 'https://bitbucket.org/owner/repo.git'

        project_configuration.set_configuration(AppConfiguration)

    class TestRedisDockerService(DockerServiceAbstract):
        image_name = u'redis'
        cmd = u'redis-server'
        container_name = u'test.redis'
        ports_mappings = [
            PortsMapping(
                host_ip=u'172.17.42.1',
                internal_port=6379
            )
        ]

    class TestPostgresqlDockerService(DockerServiceAbstract):
        image_name = u'postgresql'
        cmd = u'postgres -D'
        container_name = u'test.postgresql'
        ports_mappings = [
            PortsMapping(
                host_ip=u'172.17.42.1',
                internal_port=5432
            )
        ]

    def test_deployer_collects_config(self):
        project_service = ProjectDockerService(container_name=u'test_project')
        redis_service = self.TestRedisDockerService()
        postgresql_service = self.TestPostgresqlDockerService()

        postgresql_service.uses(redis_service)
        project_service.uses(postgresql_service, redis_service)

        deployer = DockerServiceDeployer()
        result = deployer.deploy(project_service)
        pass