#Jetee
Deployment of projects is annoying routine. But basically it consists of similar steps: clone project's repository, build its environment, install and configure nginx, supervisor, uwsgi, database and so on. So it could be automated. Such applications as Ansible, Salt-Stack provide tools to deal with it, but they come with another routine: writing deployment configuration and inventory files. It also forces you to learn their own philosophies and practices. Another important part of modern app deployment is virtualization. So it takes a lot of time to get familiar with each one in this stack. 

Jetee is a lightweight python application, which combines advantages of Ansible and Docker in a simple deployment tool supporting multiple multiple configurations.

#Installation

For now the only way to install Jetee is
	
	pip install -e git+https://github.com/WhackoJacko/Jetee.git#egg=jetee

#Quick overview

Using the following configuration file:
	
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
* running Docker container with Django project running two processes managed by supervisor

#Writing configuration file
Jetee configuration is a regular Python file. By default it's called `deployment.py`. 
##Creating configuration class
Configuration file should contain class inherited from `AppConfiguration` (by default Jetee will try to load configuration class named `Staging`) and override attributes:
####hostname
Your server hostname or ip address.
####username
Remote server's username (*default is **'root'***).
####server_names
List of server names to reference your project (used for Nginx configuration).
####project_name
Name of your project. Used for services naming, if not specified Jetee will parse it from project's repository url. 
##Defining services
Services in Jetee are central entity. They will be deployed as Docker containers.  You define primary service(which contains your project) and secondary services(databases, storages, search engines, etc.). All available services are in the namespace `jetee.service.services`.

Just override the following methods in your AppConfiguration subclass:
####get_primary_service 
Should return instance of PrimaryService.
####get_secondary_services
Should return list of any service instances.

##Defining project