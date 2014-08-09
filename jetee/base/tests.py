from unittest.case import TestCase

from jetee.base.service.docker import DockerServiceAbstract, PortsMapping


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
        import pdb;pdb.set_trace()
        print(res)