from os.path import join, dirname

from setuptools import setup


setup(
    name='jetee',
    version=0.2,
    # long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='WhackoJacko',
    entry_points={
        'console_scripts': [
            'jetee = jetee.runtime.app:dispatcher.run',
        ]
    },
    install_requires=[u'ansible', u'pyyaml'],
    # url='https://WhackoJacko@bitbucket.org/WhackoJacko/jetee.git'
)