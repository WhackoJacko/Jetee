from jetee.base.process import AbstractProcess
from jetee.base.project import AbstractProject
from jetee.processes.celery import CeleryWorkerProcess


class DjangoGunicornProcess(AbstractProcess):
    """
    Django-Gunicorn worker process
    """

    def get_command(self):
        return u'python manage.py run_gunicorn --bind unix:%s' % self.socket_filename

    def get_name(self):
        return u'web_server'


class DjangoCeleryWorkerProcess(CeleryWorkerProcess):
    """
    Django-celery worker process
    """
    initial_command = u'python manage.py celery worker'