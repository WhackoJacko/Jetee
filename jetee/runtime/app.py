#coding=utf8
import sys
import argparse

# from rebranch_deployment.docker.runtime import ServiceManager


class AppDispatcher(object):
    ACTION_CREATE = u'create'
    ACTION_UPDATE = u'update'

    args = None
    parser = None

    def _get_parser(self, ):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument(
            u'command',
            action=u'store',
            default=self.ACTION_CREATE,
            choices=[self.ACTION_CREATE, self.ACTION_UPDATE]
        )
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
        parser = self._get_parser()
        self.args = parser.parse_args(sys.argv)

    def _create(self):
        from jetee.runtime.configuration import project_configuration

        service = project_configuration.main_service

    def __init__(self):
        self._set_args()

    def run(self):
        if self.args.command == self.ACTION_CREATE:
            self._create()


dispatcher = AppDispatcher()