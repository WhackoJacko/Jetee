from __future__ import absolute_import
import os

import ansible.constants as C
from ansible.errors import AnsibleError
from ansible.inventory import Inventory
from ansible.callbacks import PlaybookRunnerCallbacks, PlaybookCallbacks, AggregateStats, display
from ansible.playbook import PlayBook
from ansible.color import ANSIBLE_COLOR, stringc

from jetee.runtime.app import dispatcher


class PlaybookRunner(object):
    @staticmethod
    def colorize(lead, num, color):
        """ Print 'lead' = 'num' in 'color' """
        if num != 0 and ANSIBLE_COLOR and color is not None:
            return "%s%s%-15s" % (stringc(lead, color), stringc("=", color), stringc(str(num), color))
        else:
            return "%s=%-4s" % (lead, str(num))

    @staticmethod
    def hostcolor(host, stats, color=True):
        if ANSIBLE_COLOR and color:
            if stats['failures'] != 0 or stats['unreachable'] != 0:
                return "%-37s" % stringc(host, 'red')
            elif stats['changed'] != 0:
                return "%-37s" % stringc(host, 'yellow')
            else:
                return "%-37s" % stringc(host, 'green')
        return "%-26s" % host

    @staticmethod
    def set_defaults():
        C.DEFAULT_ROLES_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), u'../roles'))
        C.HOST_KEY_CHECKING = False

    @classmethod
    def run(cls, playbook_config, username, password, hostname, port):
        """

        :param list host_list:
        :param playbook_config:
        :return: :raise errors.AnsibleError:
        """
        cls.set_defaults()
        print(playbook_config)
        inventory = Inventory([u'%s:%s' % (hostname, port)])
        # let inventory know which playbooks are using so it can know the basedirs
        inventory.set_playbook_basedir(os.path.dirname(playbook_config.filename))
        stats = AggregateStats()
        playbook_cb = PlaybookCallbacks(verbose=dispatcher.args.verbosity)
        runner_cb = PlaybookRunnerCallbacks(stats, verbose=dispatcher.args.verbosity)

        pb = PlayBook(
            playbook=playbook_config.filename,
            module_path=None,
            inventory=inventory,
            forks=5,
            remote_user=username,
            remote_pass=password,
            callbacks=playbook_cb,
            runner_callbacks=runner_cb,
            stats=stats,
            timeout=10,
            transport=u'smart',
            sudo=False,
            sudo_user=u'root',
            sudo_pass=None,
            extra_vars={},
            private_key_file=None,
            only_tags=[u'all'],
            skip_tags=None,
            check=False,
            diff=False,
            su=False,
            su_pass=None,
            su_user=u'root',
            vault_password=None,
            force_handlers=None
        )

        failed_hosts = []
        unreachable_hosts = []

        try:

            pb.run()

            hosts = sorted(pb.stats.processed.keys())
            playbook_cb.on_stats(pb.stats)

            for h in hosts:
                t = pb.stats.summarize(h)

                display("%s : %s %s %s %s" % (
                    cls.hostcolor(h, t),
                    cls.colorize('ok', t['ok'], 'green'),
                    cls.colorize('changed', t['changed'], 'yellow'),
                    cls.colorize('unreachable', t['unreachable'], 'red'),
                    cls.colorize('failed', t['failures'], 'red')),
                        screen_only=True
                )

                display("%s : %s %s %s %s" % (
                    cls.hostcolor(h, t, False),
                    cls.colorize('ok', t['ok'], None),
                    cls.colorize('changed', t['changed'], None),
                    cls.colorize('unreachable', t['unreachable'], None),
                    cls.colorize('failed', t['failures'], None)),
                        log_only=True
                )

            print ""
            if len(failed_hosts) > 0:
                return 2
            if len(unreachable_hosts) > 0:
                return 3
        except AnsibleError as e:
            display("ERROR: %s" % e, color='red')
            return 1