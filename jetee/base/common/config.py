

class AnsibleTaskConfig(object):
    filename = None
    variables = None

    def __init__(self, filename, variables=None):
        self.filename = filename
        self.variables = variables


    def __repr__(self):
        return 'AnsibleTaskConfig object <{}>'.format(self.filename)


class AnsibleRoleConfig(object):
    config = None

    def __init__(self, config):
        self.config = config

    def __repr__(self):
        return 'AnsibleRoleConfig object <{}>'.format(self.config[0][u'role'])