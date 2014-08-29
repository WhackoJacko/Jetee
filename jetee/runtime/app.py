#coding=utf8
from __future__ import absolute_import
import sys
import argparse

from ansible import utils

from jetee.common.shell import InteractiveShell

__all__ = [u'AppDispatcher']


class VAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        # print 'values: {v!r}'.format(v=values)
        if values == None:
            values = '1'
        try:
            values = int(values)
        except ValueError:
            values = values.count('v') + 1
        setattr(args, self.dest, values)


class AppDispatcher(object):
    ACTION_CREATE = u'create'
    ACTION_UPDATE = u'update'
    ACTION_SHELL = u'shell'

    args = None
    parser = None

    def _get_parser(self, ):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument(
            u'command',
            action=u'store',
            default=self.ACTION_CREATE,
            choices=[self.ACTION_CREATE, self.ACTION_UPDATE, self.ACTION_SHELL]
        )
        parser.add_argument('-v', nargs='?', action=VAction, dest='verbosity', help=u'Verbosity level')
        parser.add_argument(
            u'-n',
            u'--configuration_name',
            action=u'store',
            default=u'Staging',
            help=u'Project configuration class name'
        )
        parser.add_argument(
            u'-m',
            u'--configuration_module',
            default=u'deployment'
        )
        return parser

    def _set_args(self):
        args = sys.argv[1:]
        parser = self._get_parser()
        self.args = parser.parse_args(args)
        utils.VERBOSITY = self.args.verbosity

    def _create(self):
        from jetee.runtime.configuration import project_configuration

        project_configuration.get_service().deploy()
        project_configuration.get_service().project.deploy()

    def _shell(self):
        from jetee.runtime.configuration import project_configuration

        service = project_configuration.get_service()
        port = service.get_container_port()
        InteractiveShell(
            project_configuration.hostname,
            port,
            project_configuration.username,
            project_configuration.get_service().project.get_env_variables()
        ).run_shell()


    def __init__(self):
        self._set_args()

    def run(self):
        if self.args.command == self.ACTION_CREATE:
            self._create()
        elif self.args.command == self.ACTION_SHELL:
            self._shell()


dispatcher = AppDispatcher()