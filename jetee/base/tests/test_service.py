from unittest import TestCase

from jetee.base.service import PortsMapping
from jetee.base.tests.base import FakeAppTestCase, FakeDockerService


class AbstractDockerServiceTestCase(FakeAppTestCase):
    def test_service_extracts_container_name_from_image_properly(self):
        service = FakeDockerService()
        self.assertEqual(service.container_name, u'fake')

    def test_service_uses_manually_set_container_name(self):
        service = FakeDockerService(container_name=u'custom-fake-name')
        self.assertEqual(service.container_name, u'custom-fake-name')

    def test_service_container_full_name_assembled_properly(self):
        service = FakeDockerService(container_name=u'custom-fake-name')
        self.assertEqual(service.container_full_name, u'test-name-custom-fake-name')


class PortsMappingTestCase(TestCase):
    def test_ports_mapping_renders_ports_representation_properly(self):
        ports_mapping = PortsMapping(
            interface=u'123.0.0.9',
            internal_port=u'1234',
            external_port=u'4321',
            protocol=u'udp'
        )
        self.assertEqual(ports_mapping.get_representation(), u'123.0.0.9:4321:1234/udp')