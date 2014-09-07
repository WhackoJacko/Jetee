from jetee.base.process import ProcessAbstract


class CustomProcess(ProcessAbstract):
    command = None

    def get_command(self):
        return self.command


class UWSGIProcess(ProcessAbstract):
    port = 9000

    def __init__(self, wsgi_file):
        self.wsgi_file = wsgi_file

    def get_name(self):
        return u'web_server'

    def get_command(self):
        return u'uwsgi --http :%i --wsgi-file %s' % (self.port, self.wsgi_file)


class DjangoGunicornProcess(ProcessAbstract):
    port = 9000

    def get_command(self):
        return u'./manage.py run_gunicorn --bind 127.0.0.1:%i' % self.port


class CeleryWorkerProcess(ProcessAbstract):
    initial_command = u'celery worker'

    def __init__(self, app, queues=None, broker=None, concurrency=4, beat=False):
        self.app = app
        self.queues = queues
        self.broker = broker
        self.concurrency = concurrency
        self.beat = beat

    def get_name(self):
        return u'celery_tasks'

    def get_command(self):
        command = self.initial_command
        if self.app:
            command += u' --app=%s' % self.app
        if self.queues:
            command += u' --queues=' + u','.join(self.queues)
        if self.broker:
            command += u' --broker=%s' % self.broker
        if self.concurrency:
            command += u' --concurrency=%i' % int(self.concurrency)
        if self.beat:
            command += u' --beat'
        return command


class DjangoCeleryWorkerProcess(CeleryWorkerProcess):
    initial_command = u'./manage.py celery worker'