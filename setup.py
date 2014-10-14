import sys
from setuptools import setup

# trick for ReadTheDocs builder
if u'setup.py' in sys.argv:
    required_packages = [
        u'ecdsa',
    ]
else:
    required_packages = [
        u'ecdsa',
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
    install_requires=required_packages,
    url='https://github.com/WhackoJacko/Jetee.git'
)