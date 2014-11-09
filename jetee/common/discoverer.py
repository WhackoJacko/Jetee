#!/usr/bin/python
import paramiko

from jetee.runtime.configuration import project_configuration


class ConsulDiscoverer(object):
    dig_executable = u'dig'

    def discover(self, key):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(project_configuration.hostname, username=project_configuration.username)
        command = u'%s @172.17.42.1 -t SRV +noall +answer %s' % (self.dig_executable, key)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.readline().strip()
        assert bool(output)
        port = output.split()[-2]
        ssh.close()
        return int(port)