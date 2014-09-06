import os
import errno
import subprocess

from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup


def galaxy_packages_wrapper(cls):
    def run(self):
        original_run(self)
        from jetee import base

        roles_dir = os.path.join(os.path.dirname(__file__), u'jetee/roles')
        try:
            os.makedirs(roles_dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(roles_dir):
                pass
            else:
                raise
        subprocess.call(
            [u'ansible-galaxy', u'install', u'--force', u'-p', roles_dir] + list(base.REQUIRED_ANSIBLE_ROLES))

    original_run = cls.run
    cls.run = run
    return cls


setup(
    name='jetee',
    version=0.5,
    # long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='WhackoJacko',
    cmdclass={
        u'install': galaxy_packages_wrapper(install),
        u'develop': galaxy_packages_wrapper(develop)
    },

    entry_points={
        'console_scripts': [
            'jetee = jetee.runtime.app:dispatcher.run',
        ]
    },
    install_requires=[
        u'ansible',
        u'pyyaml',
        u'fabric',
        u'ecdsa'
    ],
    url='https://github.com/WhackoJacko/Jetee.git'
)