from jetee.base.process import ProcessAbstract

class CustomProcess(ProcessAbstract):
    """
    Custom python process

    Be sure to override :attr:`command` and :attr:`process_name` attributes
    """
    command = None
    process_name = None

    def get_command(self):
        return self.command

    def get_name(self):
        return self.process_name


from jetee.processes.celery import *
from jetee.processes.cron import *
from jetee.processes.django import *
from jetee.processes.uwsgi import *