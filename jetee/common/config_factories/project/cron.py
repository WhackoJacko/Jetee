import copy

from jetee.base.config_factory import AnsiblePreTaskConfigFactory
from jetee.processes import CronProcess


class CronPreTaskConfigFactory(AnsiblePreTaskConfigFactory):
    template = {
        u'cron': {
            u'name': u'',
            u'month': u'',
            u'day': u'',
            u'hour': u'',
            u'minute': u'',
            u'job': u''
        }
    }

    def get_config(self, parent):
        project = parent
        config = []
        for process in project.helper_processes:
            if isinstance(process, CronProcess):
                for job in process.jobs:
                    tmp_template = copy.deepcopy(self.template)
                    tmp_template[u'cron'][u'name'] = job.name
                    tmp_template[u'cron'][u'month'] = job.month
                    tmp_template[u'cron'][u'day'] = job.day
                    tmp_template[u'cron'][u'hour'] = job.hour
                    tmp_template[u'cron'][u'minute'] = job.minute
                    tmp_template[u'cron'][u'job'] = job.command
                    config.append(tmp_template)
        return config