from jetee.base.process import ProcessAbstract
from jetee.base.project import ProjectAbstract
from jetee.processes.celery import CeleryWorkerProcess


class DjangoGunicornProcess(ProcessAbstract):
    """
    Django-Gunicorn worker process
    """

    def get_command(self):
        return u'python manage.py run_gunicorn --bind unix:%s' % ProjectAbstract.socket_filename

    def get_name(self):
        return u'web_server'


class DjangoCeleryWorkerProcess(CeleryWorkerProcess):
    """
    Django-celery worker process
    """
    initial_command = u'python manage.py celery worker'