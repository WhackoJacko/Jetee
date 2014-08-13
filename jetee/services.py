from jetee.base.service import DockerServiceAbstract, PortsMapping
from jetee.runtime.configuration import project_configuration

__all__ = [u'AppService', u'PostgreSQLService', u'RedisService']


class AppService(DockerServiceAbstract):
    image_name = u'whackojacko/blank'
    cmd = u'supervisord --nodaemon'
    ports_mappings = [
        PortsMapping(internal_port=22, host_ip=u'0.0.0.0'),  #for sshd
        PortsMapping(internal_port=9000, host_ip=u'172.17.42.1')  #for project itself
    ]

    @property
    def container_name(self):
        if self._container_name:
            return self._container_name
        else:
            container_name = u'.'.join([project_configuration.get_project_name(), u'project'])
            return container_name


class PostgreSQLService(DockerServiceAbstract):
    image_name = u'zumbrunnen/postgresql'
    cmd = u'postgres -D'
    ports_mappings = [
        PortsMapping(
            host_ip=u'172.17.42.1',
            internal_port=5432
        )
    ]


class RedisService(DockerServiceAbstract):
    image_name = u'redis'
    cmd = u'redis-server'
    ports_mappings = [
        PortsMapping(
            host_ip=u'172.17.42.1',
            internal_port=6379
        )
    ]