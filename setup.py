import subprocess

from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup


def galaxy_packages_wrapper(cls):
    def run(self):
        original_run(self)
        from jetee import base

        subprocess.call([u'ansible-galaxy', 'install'] + list(base.REQUIRED_ANSIBLE_ROLES))

    original_run = cls.run
    cls.run = run
    return cls


setup(
    name='jetee',
    version=0.3,
    # long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='WhackoJacko',
    cmdclass={
        'install': galaxy_packages_wrapper(install),
        u'develop': galaxy_packages_wrapper(develop)
    },

    entry_points={
        'console_scripts': [
            'jetee = jetee.runtime.app:dispatcher.run',
        ]
    },
    install_requires=[u'ansible', u'pyyaml', u'fabric'],
    # url='https://WhackoJacko@bitbucket.org/WhackoJacko/jetee.git'
)