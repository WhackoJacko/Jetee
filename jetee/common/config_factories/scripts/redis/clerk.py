#!/usr/bin/env python
import os
from optparse import OptionParser, Option
from copy import copy
import redis


def ports_bindings_parser(option, opt, value):
    class PortsBinding(object):
        interface = None
        external_port = None
        internal_port = None

    port_bindings = []
    for port_binding_raw in value.split(','):
        port_binding_raw = port_binding_raw.strip()
        port_binding = PortsBinding()
        port_binding.interface, port_binding.external_port, port_binding.internal_port = port_binding_raw.split(':')
        port_bindings.append(port_binding)
    return port_bindings


class PortsBindingsOption(Option):
    """
    Custom option for ports bindings parsing
    """
    TYPES = Option.TYPES + ("ports_bindings",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["ports_bindings"] = ports_bindings_parser


class RedisClerk(object):
    options = None

    def __init__(self):
        options, _ = parser.parse_args()
        self.options = options
        self.redis_cli = redis.StrictRedis(host='localhost', port=6379, db=0)

    def _mk_value(self, key, value):
        self.redis_cli.set(key, value)

    def _rm_value(self, key, value):
        self.redis_cli.delete(key)

    def _normalize_container_name(self, container_name):
        container_name = container_name.replace(".", "/")
        return container_name

    def set_container_id(self, container_name, container_id):
        key = os.path.join(container_name, u'id')
        self._mk_value(key=key, value=container_id)

    def set_container_ports_bindings(self, container_name, ports_bindings):
        for ports_binding in ports_bindings:
            key = os.path.join(container_name, u'ports', ports_binding.internal_port)
            self._mk_value(key=os.path.join(key, u'interface'), value=ports_binding.interface)
            self._mk_value(key=os.path.join(key, u'external_port'), value=ports_binding.external_port)

    def register(self):
        container_name = self._normalize_container_name(self.options.container_name)
        self.set_container_id(container_name=container_name, container_id=self.options.container_id)
        self.set_container_ports_bindings(container_name=container_name, ports_bindings=self.options.ports_bindings)


parser = OptionParser(option_class=PortsBindingsOption)
parser.add_option("--container_id", help="Docker container ID", dest="container_id")
parser.add_option("--container_name", help="Docker container name", dest="container_name")
parser.add_option("--ports", help="Docker container external ports", type="ports_bindings", dest="ports_bindings")

if __name__ == u'__main__':
    RedisClerk().register()