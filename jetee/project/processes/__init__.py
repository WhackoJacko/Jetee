from jetee.base.process import ProcessAbstract

__author__ = 'whackojacko'


class PythonProcess(ProcessAbstract):
    def __init__(self, executable):
        self.executable = executable

    def get_command(self):
        return u'python %s' % self.executable

    def get_name(self):
        return u'web_server'


class CustomProcess(ProcessAbstract):
    command = None
    process_name = None

    def get_command(self):
        return self.command

    def get_name(self):
        return self.process_name


from .celery import *
from cron import *
from django import *
from uwsgi import *