#!/usr/bin/env python
import subprocess
import os
from optparse import OptionParser, Option
from copy import copy


def ports_bindings_parser(option, opt, value):
    class PortsBinding(object):
        host_ip = None
        external_port = None
        internal_port = None

    port_bindings = []
    for port_binding_raw in value.split(','):
        port_binding_raw = port_binding_raw.strip()
        port_binding = PortsBinding()
        port_binding.host_ip, port_binding.external_port, port_binding.internal_port = port_binding_raw.split(':')
        port_bindings.append(port_binding)
    return port_bindings


class PortsBindingsOption(Option):
    """
    Custom option for ports bindings parsing
    """
    TYPES = Option.TYPES + ("ports_bindings",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["ports_bindings"] = ports_bindings_parser


class ETCDRegistrator(object):
    options = None
    etcdctl_executable = "etcdctl"

    def __init__(self):
        options, _ = parser.parse_args()
        self.options = options

    def _call(self, *args):
        print args
        subprocess.call(args)

    def _set_dir(self, dir_name):
        self._call(*[self.etcdctl_executable, "setdir", dir_name])

    def _rm_dir(self, dir_name):
        self._call(*[self.etcdctl_executable, "rmdir", dir_name])

    def _mk_value(self, key, value):
        self._call(*[self.etcdctl_executable, "mk", key, value])

    def _rm_value(self, key, value):
        self._call(*[self.etcdctl_executable, "rm", key, value])

    def _normalize_container_name(self, container_name):
        container_name = container_name.replace(".", "/")
        return container_name

    def create_container_dir(self, container_name):
        self._set_dir(container_name)

    def set_container_id(self, container_name, container_id):
        key = os.path.join(container_name, u'id')
        self._mk_value(key=key, value=container_id)

    def set_container_ports_bindings(self, container_name, ports_bindings):
        for ports_binding in ports_bindings:
            key = os.path.join(container_name, u'ports', ports_binding.internal_port)
            value = u'{}:{}'.format(ports_binding.host_ip, ports_binding.external_port)
            self._mk_value(key=key, value=value)

    def register(self):
        container_name = self._normalize_container_name(self.options.container_name)
        self.create_container_dir(container_name=container_name)
        self.set_container_id(container_name=container_name, container_id=self.options.container_id)
        self.set_container_ports_bindings(container_name=container_name, ports_bindings=self.options.ports_bindings)


parser = OptionParser(option_class=PortsBindingsOption)
parser.add_option("--container_id", help="Docker container ID", dest="container_id")
parser.add_option("--container_name", help="Docker container name", dest="container_name")
parser.add_option("--ports", help="Docker container external ports", type="ports_bindings", dest="ports_bindings")

if __name__ == u'__main__':
    ETCDRegistrator().register()