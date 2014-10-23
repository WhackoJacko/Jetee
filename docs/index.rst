*****
Jetee
*****

Deployment of projects is annoying routine. But basically it consists of similar steps: clone project's repository, build its environment, install and configure nginx, supervisor, uwsgi, database and so on. So it could be automated. Such applications as Ansible, Salt-Stack provide tools to deal with it, but they come with another inconvenience: writing deployment configuration and inventory files. It also forces you to learn their own philosophies and practices. Another important part of modern app deployment is virtualization. So it takes a lot of time to get familiar with each one in this stack.

Jetee is a lightweight python application, which combines advantages of Ansible and Docker in a simple deployment tool supporting multiple configurations.

The basic idea of Jette - easily and rapidly deployable infrastructure. This is done by means of `Docker`. Necessary services
(databases, storages, etc.) are deployed from the Docker Registry(and are called `Secondary Services`). These are services by third party
developers and they are ready to run out of the box. The project itself is also deployed as Docker container, but its
contents are defined by user. This service is called `Primary Service`. After deployment, each image is available for
another through TCP and IP-address can be obtained via the local DNS server. All operations with the service, as well as
with the project within the primary service performed by a `Ansible`.

How it works
############

You just write the configuration file and launch the deployment process (build or update, depending on your needs).

Using the following configuration file::

    from jetee.common.user_configuration import AppConfiguration
    from jetee.service.services.primary import PrimaryService
    from jetee.service.services.postgresql import PostgreSQLService
    from jetee.service.services.redis import RedisService
    from jetee.project.projects import DjangoProject
    from jetee.project.processes import UWSGIProcess, CustomProcess

    class Staging(AppConfiguration):
        hostname = 'example.com'
        username = 'root'
        server_names = ['example.com', 'another-example.com']

        def get_primary_service(self):
            return PrimaryService(
                project=DjangoProject(
                    cvs_repo_url=u'git@github.com:example/project.git',
                    cvs_repo_branch=u'staging',
                    processes=[
                        UWSGIProcess(wsgi_file=u'project/wsgi.py'),
                        CustomProcess(command=u'python rq_worker.py')
                    ]
                )
            )

        def get_secondary_services(self):
            return [PostgreSQLService(), RedisService()]

Jetee will deploy stable infrastructure containing:

* running PostgreSQL Docker container
* running Redis Docker container
* running Debian Docker container with Django project running two processes managed by supervisor

Installation
############

Install from PyPI::

    pip install jetee

Or install the in-development version::

    pip install -e git+https://github.com/WhackoJacko/Jetee.git#egg=jetee

Writing configuration file
##########################

Jetee configuration file is a regular Python file. By default it's called ``deployment.py``.
Create a new one in the root directory of your project (location does not matter, but it's more convenient).

Creating configuration class
****************************
Configuration class is a class inherited from ``AppConfiguration``. This is the configuration of the remote server.
All deployment options are defined in it. Thereby each class inherited from ``AppConfiguration`` is a configuration.
So you may want to have multiple configuration classes(eg for staging and production servers).
By default Jetee will try to load configuration class named ``Staging``.

Defining server configuration
-----------------------------

You need to define the following attributes:

.. attribute:: AppConfiguration.hostname

    Your server hostname or ip address.

.. attribute:: AppConfiguration.username

    Remote server's username (default is `root`).

.. attribute:: AppConfiguration.server_names

    List of server names to reference your project (used for Nginx configuration).

.. attribute:: AppConfiguration.project_name

    Name of your project. Used for services naming, if not specified Jetee will parse it from project's repository url
    (eg. having repo url ``git@github.com:example/example-project.git`` project name will be ``example-project``).

Defining services
-----------------
Services in Jetee are central entity. They will be deployed as Docker containers.
You should define primary service (which contains your project) and secondary services(databases, storages, search engines, etc.). All available services are in the namespace `jetee.service.services`.
Just override the following methods in your ``AppConfiguration`` subclass:

.. py:method:: AppConfiguration.get_primary_service

    Should return an instance of PrimaryService.

.. py:method:: AppConfiguration.get_secondary_services

    Should return a list of service instances.

Defining project
----------------
Project is the filling of Primary Service. Currently this may be DjangoProject or PythonProject(which is suitable for
such frameworks as Flask, Tornado, etc.). Project instance (DjangoProject or PythonProject depending on your project`s type) must
be passed as keyword argument to the Primary Service. All needed parameters should be passed to project's class init function.

.. attribute:: Project.cvs_repo_url

    Your project's repository URL

.. attribute:: Project.cvs_repo_branch

    Branch name to checkout, this also can be the full 40-character SHA-1 hash, the literal string HEAD, or a tag name.

.. attribute:: Project.processes

    A list of processes that should be run in the primary service.

.. attribute:: Project.env_variables

    Dictionary of environment variables to be set for each process.

.. attribute:: Project.apt_packages

    List of packages that should be installed using apt.

API Reference
#############
.. toctree::
jetee.service
    jetee.project
    jetee.processes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`