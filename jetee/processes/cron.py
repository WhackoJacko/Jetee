from jetee.base.process import ProcessAbstract


class CronProcess(ProcessAbstract):
    """
    Cron process

    Takes a list of :class:`.CronJob` instances
    """

    def __init__(self, jobs):
        self.jobs = jobs

    def get_command(self):
        return u'/usr/sbin/cron -f'

    def get_name(self):
        return u'cron'


class CronJob(object):
    """
    Cron job for :class:`.CronProcess`
    """
    name = u''
    month = u''
    day = u''
    hour = u''
    minute = u''
    command = u''

    def __init__(self, name, month=u'*', day=u'*', hour=u'*', minute=u'*', command=u''):
        self.name = name
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.command = command