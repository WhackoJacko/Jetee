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
    from jetee.processes import UWSGIProcess, CustomProcess

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

Jetee configuration file is a regular Python file, containing configuration class(or classes). Once launched Jetee will
import it as python module(by default called ``deployment``).
Create a new one named `deployment.py` in the root directory of your project (location does not matter, but it's more convenient).

Creating configuration class
****************************
Configuration class is a class inherited from ``AppConfiguration``. This is the configuration of the remote server.
All deployment options are defined in it. Thereby each class inherited from ``AppConfiguration`` is a configuration
(class name is a configuration name).
So you may want to have multiple configuration classes(eg for staging and production servers).
By default Jetee will try to load configuration class named ``Staging``.

Defining server configuration
-----------------------------
In your configuration module subclass ``AppConfiguration`` and override the following attributes:

.. attribute:: AppConfiguration.hostname

    Your server hostname or ip address.

.. attribute:: AppConfiguration.username

    Remote server's username (default is `root`).

.. attribute:: AppConfiguration.server_names

    List of server names to reference your project (used for Nginx configuration).

.. attribute:: AppConfiguration.project_name

    Name of your project. Used for services naming, if not specified Jetee will parse it from project's repository url
    (eg. having repo url ``git@github.com:example/example-project.git`` project name will be ``example-project``).

So you`ll have something like this::

    from jetee.common.user_configuration import AppConfiguration

    class Staging(AppConfiguration):
        hostname = 'example.com'
        username = 'root'
        server_names = ['example.com', 'another-example.com']

As already mentioned, ``project_name`` is the optional attribute, so it would be parsed from the repo url.


Now you have to implement two methods. They are ``get_primary_service`` and ``get_secondary_services``. Here we go.

Defining services
-----------------
Services in Jetee are central entity. They are deployed as Docker containers.
You should define primary service (Ubuntu container which will contain your project) and secondary services
(databases, storages, search engines, etc.). All available services are in the namespace ``jetee.service.services``.
Just implement the following methods in your ``AppConfiguration`` subclass:

.. py:method:: AppConfiguration.get_primary_service

    Should return an instance of PrimaryService.

.. py:method:: AppConfiguration.get_secondary_services

    Should return a list of service instances.

Suppose your project uses PostgreSQL as database server, Redis as key-value storage, and ElasticSearch as search-engine
backend. This is dead simple::

    from jetee.common.user_configuration import AppConfiguration
    from jetee.service.services.primary import PrimaryService
    from jetee.service.services.postgresql import PostgreSQLService
    from jetee.service.services.redis import RedisService
    from jetee.service.services.elastic_search import ElasticSearchService

    class Staging(AppConfiguration):
        hostname = 'example.com'
        username = 'root'
        server_names = ['example.com', 'another-example.com']

        def get_primary_service(self):
            return PrimaryService()

        def get_secondary_services(self):
            return [PostgreSQLService(), RedisService(),ElasticSearchService()]

At this stage, configuration of `external` layer is done. It remains to configure `internal`.

Defining project
----------------
Project is the filling of Primary Service. It defines the sources of your app, processes to run using this sources,
packages to install for this processes and environment variables to inject(for this processes too).
Project instance must be passed as `keyword argument` to the Primary Service.
All needed parameters should be passed to project's class init function.

.. attribute:: Project.cvs_repo_url

    Your project's repository URL

.. attribute:: Project.cvs_repo_branch

    Branch name to checkout, this also can be the full 40-character SHA-1 hash, the literal string HEAD, or a tag name.

.. attribute:: Project.env_variables

    Dictionary of environment variables to be set for each process.

.. attribute:: Project.apt_packages

    List of packages that should be installed using apt.

.. attribute:: Project.processes

    A list of processes that should be run in the primary service. Read the next part to know what it is and how is it
    configured.

Defining processes
------------------
Process is the end point on the way to configure Jetee.  This is for which services have been deployed and the app was
cloned and packages were installed. Of course, you will have at least one process that provides the web server and will
be associated with Nginx, but also may require additional (a worker, planners, etc.). All of them will be deployed in Primary
Service, and their work will support Supervisor. Pass the list of instances of processes to the Project ``__init__`` method.

Suppose that our project is written with Flask. In addition to the web-server Celery worker is required for asynchronous
tasks::

    /project
        /project.py
        /celery.py
        ....

Then finally our fully working configuration will look like this::

    from jetee.common.user_configuration import AppConfiguration
    from jetee.service.services.primary import PrimaryService
    from jetee.service.services.postgresql import PostgreSQLService
    from jetee.service.services.redis import RedisService
    from jetee.service.services.elastic_search import ElasticSearchService
    from jetee.processes import UWSGIProcess, CeleryWorkerProcess

    class Staging(AppConfiguration):
        hostname = 'example.com'
        username = 'root'
        server_names = ['example.com', 'another-example.com']

        def get_primary_service(self):
            return PrimaryService(
                cvs_repo_url=u'git@github.com:example/project.git',
                cvs_repo_branch=u'staging',
                processes=[
                    UWSGIProcess(wsgi_module=u'project:app'),
                    CeleryWorkerProcess(app=u'app', queues=[u'email', u'statistics'])
                ]
            )

        def get_secondary_services(self):
            return [PostgreSQLService(), RedisService(),ElasticSearchService()]

Launching Jetee
###############
Once the configuration file is ready, you are ready to deploy the app.

To deploy the services launch::

    jetee build service

Once services are deployed, you can start deploying the project within the Primary Service::

    jetee build project

Jetee will ask you to add a deployment key of the server and set up the project. That's all!


There is a command which deploys from beginning to end(this is equivalent to the consecutive launch of
``jetee build service`` and ``jetee build project``)::

    jetee build all

Of course, you'll need to update your project from time to time::

    jetee update project

If something goes wrong, you can connect to your Primary Service container via SSH::

    jetee ssh

Specifying launch options
*************************
By default Jetee will try to import configuration class named ``Staging`` from module named deployment(therefore file
should have name `deployment.py`). To specify custom configuration name use `-n` key, to specify module name use `-m`
key. For example::

    jetee build all -m my_deployment -n Production

Jetee will try to import module named `my_deployment` and its class named `Production`.

Configuring your app to work in Jetee environment
#################################################

The architecture of the environment requires some changes to your application.

Defining current configuration
******************************
To help your application to define in which configuration it is running, Jetee injects environment variable containing the
name of the current configuration, for each process as well as for the SSH session. For DjangoProject this variable is
called ``DJANGO_CONFIGURATION``, for PythonProject  - ``CONFIGURATION``. See django-configurations_
app to learn how to use this type of flag effectively.

.. _django-configurations: http://django-configurations.readthedocs.org/en/latest/

Configuring your app to get connected with services
***************************************************
Deployed services are registered in Consul_ via Registrator_ service. Each running service is registered under the name
of the form `<project_name>-<service_name>`. After that, all the services available to each other via a local DNS service.
This allows you to define the port and IP-address of any registered service.
To rid yourself of the difficulties of configuration use Jetee-tools_.

.. _Consul: https://www.consul.io/
.. _Registrator: https://github.com/progrium/registrator
.. _Jetee-tools: http://jetee-tools.readthedocs.org/en/latest/


Serving media and static files
******************************
Jetee configures nginx for serving static and media files. Static files should be collected in `/app/static/`, and
media files in `/app/media/`.

Configuration example
*********************
In summary, a very simple example that demonstrates the configuration logic might look like this::

    import os

    #get current configuration name
    configuration_name = os.getenv(u'DJANGO_CONFIGURATION', u'Development')

    #Django database settings
    if configuration_name == u'Production':
        from jetee_tools.service_resolvers import DjangoDatabaseJeteeServiceConfigResolver
        #Production settings go there
        DATABASES = {
            'default': DjangoDatabaseJeteeServiceConfigResolver(
                host=u'my-project-postgresql',
                protocol=u'postgresql_psycopg2'
            ).render()
        }
    else:
        #Development settings go there
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': u'example',
                'USER': u'example',
                'PASSWORD': None,
                'HOST': 'localhost',
                'PORT': 5432,
            },
        }

Toolkit
#######
Here is the list of available tools.

Services
********
:ref:`PrimaryService <primary-service>`


:ref:`ElasticSearchService <elasticsearch-service>`

:ref:`PostgreSQLService <postgresql-service>`

:ref:`RedisService <redis-service>`

Projects
********
:ref:`DjangoProject <projects>`

:ref:`PythonProject <projects>`

Processes
*********
:ref:`CustomProcess <custom-process>`

:ref:`CeleryWorkerProcess <celery-process>`

:ref:`UWSGIProcess <uwsgi-process>`

:ref:`DjangoGunicornProcess <django-process>`

:ref:`DjangoCeleryWorkerProcess <django-process>`

:ref:`CronProcess <cron-process>`

API Reference
#############
.. toctree::
    jetee.service
    jetee.project
    jetee.processes


Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`