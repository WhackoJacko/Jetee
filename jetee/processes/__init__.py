from jetee.base.process import ProcessAbstract


class CustomProcess(ProcessAbstract):
    """
    Custom python process

    Be sure to override :attr:`command` and :attr:`process_name` attributes
    """
    command = None
    name = None

    def __init__(self, command, name, env_variables=None):
        self.command = command
        self.name = name
        self.env_variables = env_variables or {}

    def get_command(self):
        return self.command

    def get_name(self):
        return self.name


from jetee.processes.celery import *
from jetee.processes.cron import *
from jetee.processes.django import *
from jetee.processes.uwsgi import *