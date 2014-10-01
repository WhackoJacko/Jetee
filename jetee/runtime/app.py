#coding=utf8
from __future__ import absolute_import
import sys
import argparse
import warnings

from ansible import utils

from jetee.common.shell import InteractiveShell
from jetee.service.deployment_managers import DockerServiceDeploymentManager
from jetee.project.deployment_managers import ProjectDeploymentManager

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
    ACTION_BUILD = u'build'
    ACTION_UPDATE = u'update'
    ACTION_SSH = u'ssh'

    TARGET_SERVICE = u'service'
    TARGET_PROJECT = u'project'

    service_deployment_manager = DockerServiceDeploymentManager
    project_deployment_manager = ProjectDeploymentManager

    args = None
    parser = None

    def _get_parser(self, ):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument(
            u'action',
            action=u'store',
            default=self.ACTION_BUILD,
            choices=[self.ACTION_BUILD, self.ACTION_UPDATE, self.ACTION_SSH]
        )
        parser.add_argument(
            u'target',
            nargs='?',
            action=u'store',
            default=self.TARGET_PROJECT,
            choices=[self.TARGET_SERVICE, self.TARGET_PROJECT]
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

    def _build_service(self):
        from jetee.runtime.configuration import project_configuration

        self.service_deployment_manager().deploy(project_configuration)
        self.project_deployment_manager().deploy(project_configuration)

    def _build_project(self):
        from jetee.runtime.configuration import project_configuration

        self.project_deployment_manager().deploy(project_configuration)

    def _update_project(self):
        from jetee.runtime.configuration import project_configuration

        self.project_deployment_manager().update(project_configuration)

    def _ssh(self):
        from jetee.runtime.configuration import project_configuration

        service = project_configuration.get_primary_service()
        port = service.get_container_port()
        InteractiveShell(
            project_configuration.hostname,
            port,
            project_configuration.username,
            service.project.get_env_variables()
        ).run_ssh()


    def __init__(self):
        self._set_args()

    def run(self):
        if self.args.action == self.ACTION_BUILD:
            if self.args.target == self.TARGET_SERVICE:
                self._build_service()
            else:
                self._build_project()
        elif self.args.action == self.ACTION_UPDATE:
            self._update_project()
        elif self.args.action == self.ACTION_SSH:
            self._ssh()


dispatcher = AppDispatcher()