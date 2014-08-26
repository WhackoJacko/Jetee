import subprocess


class InteractiveShell(object):
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port
        self.username = username

    def run_shell(self):
        subprocess.call([u'ssh', u'%s@%s' % (self.username, self.hostname), u'-p', unicode(self.port)])