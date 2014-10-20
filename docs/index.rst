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

Quick overview
##############

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
                        UWSGIProcess(wsgi_file=u'project/wsgi.py')
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

For now the only way to install Jetee is::

    pip install -e git+https://github.com/WhackoJacko/Jetee.git#egg=jetee


Writing configuration file
##########################

Jetee configuration file is a regular Python file. By default it's called `deployment.py`.

Creating configuration class
****************************

Configuration file should contain class inherited from `AppConfiguration` (by default Jetee will try to load configuration class named `Staging`) and override attributes:

* **hostname**
    Your server hostname or ip address.
* **username**
    Remote server's username (*default is **'root'***).
* **server_names**
    List of server names to reference your project (used for Nginx configuration).
* **project_name**
    Name of your project. Used for services naming, if not specified Jetee will parse it from project's repository url.

Defining services
-----------------
Services in Jetee are central entity. They will be deployed as Docker containers. You define primary service(which contains your project) and secondary services(databases, storages, search engines, etc.). All available services are in the namespace `jetee.service.services`.
Just override the following methods in your AppConfiguration subclass:

* **get_primary_service**
    Should return an instance of PrimaryService.
* **get_secondary_services**
    Should return a list of service instances.

Defining project
----------------
Project is the filling of Primary Service. Currently this may be DjangoProject or PythonProject(which is suitable for
such frameworks as Flask, Tornado, etc.). Project instance (DjangoProject or PythonProject depending on your needs) must
be passed as keyword argument to the Primary Service. All needed parameters should be passed to project's class init function.

* **cvs_repo_url**
    Your project's repository URL
* **cvs_repo_branch**
    Branch name to checkout, this also can be the full 40-character SHA-1 hash, the literal string HEAD, or a tag name.
* **processes**
    A list of processes that should be run in the primary service.
* **env_variables**
    Dict of environment variables to be set for each process.
* **apt_packages**
    List of packages that should be installed using apt.

API Reference
#############
.. toctree::
    :maxdepth: 6

    jetee.processes
    jetee.project
    jetee.service


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`