# import sys
# import os
# from unittest.case import TestCase
#
# from jetee.runtime.configuration import project_configuration
# from jetee.base.service import DockerServiceAbstract, PortsMapping
# from jetee.service.services import AppService
# from jetee.project.projects import DjangoProject
#
#
#
#
#
# class DockerDeployerTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         sys.argv = [u'ss', u'create', u'-vvvvv']
#         from jetee.common.user_configuration import AppConfiguration
#
#         class TestAppConfiguration(AppConfiguration):
#             hostname = os.getenv(u'JETEE_TEST_HOSTNAME')
#             username = u'root'
#             server_names = [u'example.ru']
#
#
#         project_configuration.set_configuration(TestAppConfiguration)
#
#     class TestRedisDockerService(DockerServiceAbstract):
#         image = u'redis'
#         command = u'redis-server'
#         ports_mappings = [
#             PortsMapping(
#                 interface=u'172.17.42.1',
#                 internal_port=6379
#             )
#         ]
#
#     class TestPostgresqlDockerService(DockerServiceAbstract):
#         image = u'zumbrunnen/postgresql'
#         command = u'postgres -D'
#         ports_mappings = [
#             PortsMapping(
#                 interface=u'172.17.42.1',
#                 internal_port=5432
#             )
#         ]
#
#     def test_deployer_collects_config(self):
#         project_service = AppService(project=DjangoProject(cvs_repo_url=u'https://bitbucket.org/team/repo.git'))
#         redis_service = self.TestRedisDockerService()
#         postgresql_service = self.TestPostgresqlDockerService()
#
#         postgresql_service.uses(redis_service)
#         project_service.uses(postgresql_service)
#
#         from jetee.service.deployment_managers import DockerServiceDeploymentManager
#
#         deployer = DockerServiceDeploymentManager()
#         result = deployer.deploy(project_service)
#         pass
#
#
# class ConfigFactoryTestCase(TestCase):
#     service = None
#
#     def test_config_factory(self):
#         class TestDockerService(DockerServiceAbstract):
#             image = u'test-image'
#             command = u'bash'
#             container_name = u'test-container'
#             ports_mappings = [
#                 PortsMapping(internal_port=22, external_port=49155, interface=u'0.0.0.0')
#             ]
#
#         service = TestDockerService(
#             container_name=u'test'
#         )
#         res = service.factory_deployment_config()
#         print(res)