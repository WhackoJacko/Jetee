import sys
import os
from unittest.case import TestCase

from jetee.runtime.configuration import project_configuration
from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.service.services import AppService
from jetee.project.projects import DjangoProject


class TestRedisDockerService(DockerServiceAbstract):
    image = u'redis'
    command = u'redis-server'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=6379
        )
    ]


class TestPostgresqlDockerService(DockerServiceAbstract):
    image = u'zumbrunnen/postgresql'
    command = u'postgres -D'
    ports_mappings = [
        PortsMapping(
            interface=u'172.17.42.1',
            internal_port=5432
        )
    ]


class ProjectDeployerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        sys.argv = [u'ss', u'create', u'-vvvvv']
        from jetee.common.user_configuration import AppConfiguration

        class TestAppConfiguration(AppConfiguration):
            hostname = os.getenv(u'JETEE_TEST_HOSTNAME')
            username = u'root'
            server_names = [u'example.ru']

            def get_service(self):
                project_service = AppService()
                redis_service = TestRedisDockerService()
                postgresql_service = TestPostgresqlDockerService()

                postgresql_service.uses(redis_service)
                project_service.uses(postgresql_service)
                return project_service

        project_configuration.set_configuration(TestAppConfiguration)

