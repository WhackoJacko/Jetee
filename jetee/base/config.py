class AnsibleTaskConfig(object):
    TYPE_TASK = 0
    TYPE_PRE_TASK = 1
    TYPE_POST_TASK = 2

    type = 0
    filename = None
    variables = None

    def __init__(self, filename, variables=None, type=TYPE_TASK):
        self.filename = filename
        self.variables = variables
        self.type = type

    def __repr__(self):
        return 'AnsibleTaskConfig object <{}>'.format(self.filename)

    def is_task(self):
        return self.type == self.TYPE_TASK

    def is_pre_task(self):
        return self.type == self.TYPE_PRE_TASK

    def is_post_task(self):
        return self.type == self.TYPE_POST_TASK


class AnsibleRoleConfig(object):
    config = None
    needs_merge = False

    def __init__(self, config, needs_merge):
        self.config = config
        self.needs_merge = needs_merge

    def __repr__(self):
        return 'AnsibleRoleConfig object <{}>'.format(self.config[u'role'])