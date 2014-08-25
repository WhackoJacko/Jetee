from jetee.base.config_factory import AnsibleTemplateMixin, AnsiblePreTaskConfigFactory


class GoPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    variables = {
        u'etcd_repo_location': u'/usr/local/go/src/pkg/github.com/coreos/etcd'
    }

    template = [
        {
            "name": "Download Go archive locally",
            "get_url": {
                u'url': u'https://storage.googleapis.com/golang/go1.3.1.linux-amd64.tar.gz',
                u'dest': u'/tmp/go.tgz'
            },
            u'when': u'ansible_userspace_bits == "64"'
        },
        {
            "name": "Download Go archive locally",
            "get_url": {
                u'url': u'https://storage.googleapis.com/golang/go1.3.1.linux-386.tar.gz',
                u'dest': u'/tmp/go.tgz'
            },
            u'when': u'ansible_userspace_bits == "32"'
        },
        {
            "name": "Extract Go archive to remote server",
            "unarchive": {
                u'copy': u'no',
                u'src': u'/tmp/go.tgz',
                u'dest': u'/usr/local/'
            }
        }
    ]