from jetee.base.process import ProcessAbstract
from jetee.base.project import ProjectAbstract


class CustomProcess(ProcessAbstract):
    command = None
    process_name = None

    def get_command(self):
        return self.command

    def get_name(self):
        return self.process_name


class CronProcess(ProcessAbstract):
    def get_command(self):
        return u'/usr/sbin/cron -f'

    def get_name(self):
        return u'cron'


class PythonProcess(ProcessAbstract):
    def __init__(self, executable):
        self.executable = executable

    def get_command(self):
        return u'python %s' % self.executable

    def get_name(self):
        return u'web_server'


class UWSGIProcess(ProcessAbstract):
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


class DjangoGunicornProcess(ProcessAbstract):
    def get_command(self):
        return u'python manage.py run_gunicorn --bind unix:%s' % ProjectAbstract.socket_filename

    def get_name(self):
        return u'web_server'


class CeleryWorkerProcess(ProcessAbstract):
    initial_command = u'celery worker'
    env_variables = {u'C_FORCE_ROOT': u'True'}

    def __init__(self, app=None, queues=None, broker=None, concurrency=4, beat=False):
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
    initial_command = u'python manage.py celery worker'