from setuptools import setup


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
    install_requires=[
        u'ecdsa',
        u'ansible'
    ],
    url='https://github.com/WhackoJacko/Jetee.git'
)