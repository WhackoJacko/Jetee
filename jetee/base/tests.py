import sys
import os
from unittest.case import TestCase
from deployers import DockerServiceDeployer

from jetee.runtime.configuration import project_configuration
from jetee.user_configuration import AppConfiguration
from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.services import AppService


class DockerDeployerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        sys.argv = [u'create', u'-vvvvv']

        class TestAppConfiguration(AppConfiguration):
            HOSTNAME = os.getenv(u'JETEE_TEST_HOSTNAME')
            USERNAME = u'root'
            SERVER_NAMES = [u'example.ru']
            CVS_BRANCH = u'master'
            CVS_REPO_URL = 'https://bitbucket.org/owner/jetee.git'

        project_configuration.set_configuration(TestAppConfiguration)

    class TestRedisDockerService(DockerServiceAbstract):
        image_name = u'redis'
        cmd = u'redis-server'
        ports_mappings = [
            PortsMapping(
                host_ip=u'172.17.42.1',
                internal_port=6379
            )
        ]

    class TestPostgresqlDockerService(DockerServiceAbstract):
        image_name = u'zumbrunnen/postgresql'
        cmd = u'postgres -D'
        ports_mappings = [
            PortsMapping(
                host_ip=u'172.17.42.1',
                internal_port=5432
            )
        ]

    def test_deployer_collects_config(self):
        project_service = AppService()
        redis_service = self.TestRedisDockerService()
        postgresql_service = self.TestPostgresqlDockerService()

        postgresql_service.uses(redis_service)
        project_service.uses(postgresql_service)

        deployer = DockerServiceDeployer()
        result = deployer.deploy(project_service)
        pass


class ConfigFactoryTestCase(TestCase):
    service = None

    def test_config_factory(self):
        class TestDockerService(DockerServiceAbstract):
            image_name = u'test-image'
            cmd = u'bash'
            container_name = u'test-container'
            ports_mappings = [
                PortsMapping(internal_port=22, external_port=49155, host_ip=u'0.0.0.0')
            ]

        service = TestDockerService(
            container_name=u'test'
        )
        res = service.factory_config()
        import pdb;

        pdb.set_trace()
        print(res)