class AnsibleConfig(object):
    filename = None
    variables = None

    def __init__(self, filename, variables=None):
        self.filename = filename
        self.variables = variables

    def __repr__(self):
        return 'AnsibleConfig object <{}>'.format(self.filename)