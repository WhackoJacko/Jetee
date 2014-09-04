from jetee.base.config_factory import AnsibleTemplateMixin, AnsiblePreTaskConfigFactory


class ETCDPackageAnsibleConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    repo_location = u'/usr/local/go/src/pkg/github.com/coreos/etcd'
    variables = {
        u'etcd_repo_location': u'/usr/local/go/src/pkg/github.com/coreos/etcd'
    }

    template = [
        {
            "name": "Clone etcd",
            "git": {
                u'repo': u'https://github.com/coreos/etcd',
                u'version': u'576e26ea39eae68c912b6d2c64c819fe2414b741',
                u'dest': u'{{etcd_repo_location}}'
            }
        },
        {
            "name": "Get etcd source",
            "command": "chdir=/usr/local/go/ {{etcd_repo_location}}/build",
            "environment": {
                u'PATH': u'/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin:/usr/local/go/bin'
            }
        },
        {
            "name": "Build etcd",
            "command": "chdir=/usr/local/go/ {{etcd_repo_location}}/build",
            "environment": {
                u'PATH': u'/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin:/usr/local/go/bin'
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