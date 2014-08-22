#!/usr/bin/python
import paramiko

from jetee.runtime.configuration import project_configuration
from jetee.service.scripts.etcd.clerk import ETCDClerk


class Discoverer(object):
    etcdctl_executable = ETCDClerk.etcdctl_executable

    def discover(self, key):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(project_configuration.hostname, username=project_configuration.username)
        stdin, stdout, stderr = ssh.exec_command(u'%s get %s' % (self.etcdctl_executable, key))
        port = stdout.readline().strip()
        ssh.close()
        return int(port)