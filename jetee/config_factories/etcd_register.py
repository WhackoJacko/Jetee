import os
from jetee.base.config_factory import AnsibleConfigFactory

etcd_register_script = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'scripts/etcd_register.py'))


class AnsibleETCDRegisterContainerConfigFactory(AnsibleConfigFactory):
    _template = {
        u'name': u'Register {name} container in etcd',
        u'script': etcd_register_script + u' --ports="{ports_mappings}" --container_id={container_id} --container_name={container_name}'
    }

    _ports_mapping_template = u'{{{name}_result["ansible_facts"]["docker_containers"][0]["NetworkSettings"]["Ports"]' \
                              u'["{internal_port}/tcp"][0]["HostIp"]}}:{{{name}_result["ansible_facts"]' \
                              u'["docker_containers"][0]["NetworkSettings"]["Ports"]["{internal_port}/tcp"][0]' \
                              u'["HostPort"]}}:{internal_port}'
    _container_id_template = u'{{{name}_result["ansible_facts"]["docker_containers"][0]["Id"]}}'
    _container_name = u'{{{name}_result["ansible_facts"]["docker_containers"][0]["Name"]}}'

    def _render_ports_mappings(self, service):
        ports_mappings = u''
        for ports_mapping in service.ports_mappings:
            ports_mappings += self._ports_mapping_template.format(name=service.container_name,
                                                                  internal_port=ports_mapping.internal_port)
        return ports_mappings

    def _render_container_id(self, service):
        return self._container_id_template.format(name=service.container_name)

    def _render_container_name(self, service):
        return self._container_name.format(name=service.container_name)

    def get_config(self, service):
        etcd_template = self._template.copy()
        etcd_template[u'name'] = etcd_template[u'name'].format(name=service.container_name)
        ports_mappings = self._render_ports_mappings(service)
        container_id = self._render_container_id(service)
        container_name = self._render_container_name(service)
        etcd_template[u'script'] = etcd_template[u'script'].format(
            ports_mappings=ports_mappings,
            container_id=container_id,
            container_name=container_name
        )
        return [etcd_template]