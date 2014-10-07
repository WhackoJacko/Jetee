#Jetee
Deployment of projects is annoying routine. But basically it consists of similar steps: clone project's repository, build its environment, install and configure nginx, supervisor, uwsgi, database and so on. So it could be automated. Such applications as Ansible, Salt-Stack provide tools to deal with it, but they come with another routine: writing deployment configuration and inventory files. It also forces you to learn their own philosophies and practices. Another important part of modern app deployment is virtualization. So it takes a lot of time to get familiar with each one in this stack. 

Jetee is a lightweight python application, which combines advantages of Ansible and Docker in a simple deployment tool.

#Installation:

for now the only way to install Jetee is
	
	pip -e git+https://github.com/WhackoJacko/Jetee.git#egg=jetee

#Quick start:

Using the following configuration file:


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

Jetee deploys stable infrastructure, consisting:

* running PostgreSQL Docker container
* running Redis Docker container
* running Docker container with Django project running two processes managed by supervisor

#Writing configuration file

Basically, writing Jetee config is split into 3 parts:

* filling server information(hostname, username, project`s server names)
* configuring services(databases, storages, search engines etc.)
* configuring project

## Services
Service is the docker container
