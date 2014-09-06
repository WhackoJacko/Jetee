from jetee.base.config_factory import AnsibleTemplateMixin, AnsiblePreTaskConfigFactory


class ETCDPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    repo_location = u'/usr/local/go/src/pkg/github.com/coreos/etcd'
    variables = {
        u'etcd_repo_location': u'/usr/local/go/src/pkg/github.com/coreos/etcd'
    }

    template = [
        {
            "name": "Get etcd",
            "command": "/usr/local/go/bin/go get github.com/coreos/etcd",
            "environment": {
                u'PATH': u'/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin:/usr/local/go/bin',
                u'GOPATH': u'/usr/local/go/'
            }
        },
        {
            "name": "Build etcd",
            "command": "/usr/local/go/bin/go build github.com/coreos/etcd",
            "environment": {
                u'PATH': u'/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin:/usr/local/go/bin',
                u'GOPATH': u'/usr/local/go/'
            }
        },
        {
            "name": "Start etcd",
            "command": "/usr/local/go/bin/etcd",
            "async": "3153600000",
            "poll": "0"
        }
    ]


class ETCDCtlPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    variables = {
        u'etcdctl_repo_location': u'/usr/local/go/src/pkg/github.com/coreos/etcdctl'
    }

    template = [
        {
            u'name': u'Clone etcdctl',
            u'git': u'repo=https://github.com/coreos/etcdctl.git dest={{etcdctl_repo_location}}'
        },
        {
            u'name': u'Build etcdctl',
            u'command': u'chdir=/usr/local/go/ {{etcdctl_repo_location}}/build',
            u'environment': {
                u'PATH': u'/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin:/usr/local/go/bin'
            }
        }
    ]