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
    version=0.6,
    description='Lightweight deployment tool',
    author='Sergey Dubinin',
    author_email='whackojacko.ru@gmail.com',
    url='https://github.com/WhackoJacko/Jetee.git',
    download_url='https://github.com/WhackoJacko/Jetee/archive/v0.6.tar.gz',
    entry_points={
        'console_scripts': [
            'jetee = jetee.runtime.app:dispatcher.run',
        ]
    },
    packages=find_packages(),
    install_requires=required_packages,
    classifiers=[],
)