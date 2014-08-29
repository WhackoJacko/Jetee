from jetee.base.process import ProcessAbstract


class UWSGIProcess(ProcessAbstract):
    def __init__(self, wsgi_file, port=9000):
        self.wsgi_file = wsgi_file
        self.port = port

    def get_name(self):
        return u'web_server'

    def get_command(self):
        return u'uwsgi --http :%i --wsgi-file %s' % (self.port, self.wsgi_file)