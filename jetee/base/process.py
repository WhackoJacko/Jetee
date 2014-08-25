import os


class ProcessAbstract(object):
    def get_name(self):
        raise NotImplementedError

    def get_command(self):
        raise NotImplementedError

    def get_working_directory(self):
        from jetee.runtime.configuration import project_configuration

        return os.path.join(project_configuration.get_project().location, project_configuration.get_project_name())