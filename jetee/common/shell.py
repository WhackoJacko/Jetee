import subprocess

from jetee.common.utils import render_env_variables


class InteractiveShell(object):
    def __init__(self, hostname, port, username, env_variables=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.env_variables = env_variables or {}

    def run_shell(self):
        env_variables = u'export %s; bash' % render_env_variables(self.env_variables)
        subprocess.call([
            u'ssh',
            u'-t',
            u'%s@%s' % (self.username, self.hostname),
            u'-p',
            unicode(self.port),
            env_variables
        ])