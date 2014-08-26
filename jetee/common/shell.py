import subprocess


class InteractiveShell(object):
    def __init__(self, hostname, port, username, env_variables=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.env_variables = env_variables or {}

    def render_env_variables(self, env_variables):
        rendered_env_variables = u','.join([u'{}="{}"'.format(key, value) for key, value in env_variables.items()])
        if rendered_env_variables:
            rendered_env_variables = u'export %s; bash' % rendered_env_variables
        return rendered_env_variables

    def run_shell(self):
        subprocess.call([
            u'ssh',
            u'-t',
            u'%s@%s' % (self.username, self.hostname),
            u'-p',
            unicode(self.port),
            self.render_env_variables(self.env_variables)
        ])