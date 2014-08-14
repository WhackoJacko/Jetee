class InteractiveShell(object):
    def __init__(self, hostname, port, username, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def run_shell(self):
        from fabric.api import env
        from fabric.operations import open_shell

        env.host_string = self.hostname
        env.port = self.port
        env.user = self.username
        open_shell()