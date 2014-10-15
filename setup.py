import sys
from setuptools import setup, find_packages

# trick for ReadTheDocs builder
if u'setup.py' in sys.argv:
    required_packages = [
        u'ecdsa',
        u'pyyaml',
        u'paramiko'
    ]
else:
    required_packages = [
        u'ecdsa',
        u'pyyaml',
        u'paramiko',
        u'ansible'
    ]

setup(
    name='jetee',
    version=0.5,
    # long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='WhackoJacko',
    entry_points={
        'console_scripts': [
            'jetee = jetee.runtime.app:dispatcher.run',
        ]
    },
    packages=find_packages(),
    install_requires=required_packages,
    url='https://github.com/WhackoJacko/Jetee.git'
)