import os


class ProcessAbstract(object):
    env_variables = {}

    def get_name(self):
        raise NotImplementedError

    def get_command(self):
        raise NotImplementedError

    def get_working_directory(self):
        from jetee.runtime.configuration import project_configuration

        return os.path.join(
            project_configuration.get_service().project.location,
            project_configuration.get_project_name()
        )

    def get_env_variables(self):
        return self.env_variables.copy()