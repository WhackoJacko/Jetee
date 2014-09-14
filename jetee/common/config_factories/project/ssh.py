from jetee.base.config_factory import AnsiblePreTaskConfigFactory, AnsibleTemplateMixin


class GenerateSSHKeyAndPromptUserAnsibleTaskConfigFactory(AnsibleTemplateMixin, AnsiblePreTaskConfigFactory):
    template = [

        {
            u'name': u'Generate SSH key',
            u'user': {
                u'name': u'root',
                u'generate_ssh_key': u'yes',
                u'ssh_key_bits': u'2048',
            }
        },

        {
            u'name': u'Show SSH public key',
            u'command': u'/bin/cat /root/.ssh/id_rsa.pub',
            u'register': u'key_cat'
        },
        {
            u'debug': u'var=key_cat.stdout_lines'
        },
        {
            u'name': u'Wait for user to copy SSH public key',
            u'pause': {
                u'prompt': u"Plase add the SSH public key above to your repo`s deployment keys"
            }
        }
    ]