from jetee.base.process import ProcessAbstract
from jetee.base.project import ProjectAbstract


class UWSGIProcess(ProcessAbstract):
    """
    UWSGI process
    """

    def __init__(self, wsgi_file=None, wsgi_module=None, processes=None, threads=None):
        self.wsgi_file = wsgi_file
        self.processes = processes
        self.threads = threads
        self.wsgi_module = wsgi_module

    def get_name(self):
        return u'web_server'

    def get_command(self):
        command = u'uwsgi --http-socket %s' % ProjectAbstract.socket_filename
        if self.wsgi_module:
            command += u' --wsgi %s' % self.wsgi_module
        if self.wsgi_file:
            command += u' --wsgi-file %s' % self.wsgi_file
        if self.processes:
            command += u' --processes %i' % self.processes
        if self.threads:
            command += u' --threads %i' % self.threads
        command += u' --chmod-socket=666'
        return command