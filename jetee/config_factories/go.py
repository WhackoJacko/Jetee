from jetee.base.config_factory import AnsibleTemplatedConfigFactory


class GoPackageAnsibleConfigFactory(AnsibleTemplatedConfigFactory):
    variables = {
        u'etcd_repo_location': u'/usr/local/go/src/pkg/github.com/coreos/etcd'
    }

    template = [
        {
            "name": "Download Go locally",
            "get_url": {
                u'url': u'https://storage.googleapis.com/golang/go1.3.1.linux-amd64.tar.gz',
                u'dest': u'/tmp/go.tgz'
            }
        },
        {
            "name": "Extract Go archive on remote",
            "unarchive": {
                u'copy': u'no',
                u'src': u'/tmp/go.tgz',
                u'dest': u'/usr/local/'
            }
        }
    ]