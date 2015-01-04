import re

import paramiko

from jetee.runtime.configuration import project_configuration


class ServiceDiscoverer(object):
    def __init__(self, container_name):
        self.container_name = container_name

    def extract_port(self, raw_string):
        res = re.compile(u'.*:(\d+)->22/tcp').findall(raw_string)
        return res[0]

    def discover_port(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(project_configuration.hostname, username=project_configuration.username)
        command = u'docker ps | grep \' {} \''.format(self.container_name)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.readline().strip()
        assert bool(output)
        ssh.close()
        return int(self.extract_port(output))