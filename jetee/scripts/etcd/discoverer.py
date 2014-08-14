#!/usr/bin/env python
import subprocess
from subprocess import Popen, PIPE
from optparse import OptionParser


class ETCDDiscoverer(object):
    options = None
    etcdctl_executable = "/usr/local/go/bin/etcdctl"

    def __init__(self):
        options, _ = parser.parse_args()
        self.options = options

    def _call(self, *args):
        try:
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
        except subprocess.CalledProcessError, e:
            print(e.output)
            print(e.message)
            print(e.returncode)
        else:
            return output.strip()

    def _get(self, key):
        return self._call(*[self.etcdctl_executable, "get", key])

    def discover(self):
        print self._get(self.options.key)


parser = OptionParser()
parser.add_option("--key", help="ETCD key")

if __name__ == u'__main__':
    ETCDDiscoverer().discover()