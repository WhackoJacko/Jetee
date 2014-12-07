import sys
from setuptools import setup, find_packages


setup(
    name='jetee',
    version=u'0.6.9',
    description='Lightweight deployment tool',
    author='Sergey Dubinin',
    author_email='whackojacko.ru@gmail.com',
    url='https://github.com/WhackoJacko/Jetee.git',
    download_url='https://github.com/whackojacko/jetee/tarball/v0.6.9/',
    entry_points={
        'console_scripts': [
            'jetee = jetee.runtime.app:dispatcher.run',
        ]
    },
    packages=find_packages(),
    install_requires=[
        u'ecdsa',
        u'pyyaml',
        u'paramiko'
    ],
    classifiers=[],
    include_package_data=True
)