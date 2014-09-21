#!/usr/bin/python
import paramiko

from jetee.runtime.configuration import project_configuration
from jetee.common.config_factories.scripts.etcd.clerk import ETCDClerk


class EtcdDiscoverer(object):
    etcdctl_executable = ETCDClerk.etcdctl_executable

    def discover(self, key):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(project_configuration.hostname, username=project_configuration.username)
        stdin, stdout, stderr = ssh.exec_command(u'%s get %s' % (self.etcdctl_executable, key))
        port = stdout.readline().strip()
        ssh.close()
        return int(port)


class RedisDiscoverer(object):
    redis_executable = u'redis-cli'

    def discover(self, key):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(project_configuration.hostname, username=project_configuration.username)
        stdin, stdout, stderr = ssh.exec_command(u'%s get %s' % (self.redis_executable, key))
        port = stdout.readline().strip()
        ssh.close()
        return int(port)


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