class Settings(object):
    default_values = {
        'env_files_dir': 'docker-compose-config',
        'files_dir': 'docker-compose-files',
        'mount_dir': 'docker/var',
        'extensions': [],
        'tasks': []
    }

    values = {}

    def __init__(self, values=None, *args, **kwargs):
        self.values.update(self.default_values)
        if values:
            self.values.update(values)

    @property
    def env_files_dir(self):
        return self.values.get('env_files_dir')

    @property
    def files_dir(self):
        return self.values.get('files_dir')

    @property
    def extensions(self):
        return self.values.get('extensions')

    @property
    def mount_dir(self):
        return self.values.get('mount_dir')

    @property
    def tasks(self):
        return self.values.get('tasks')

    def __str__(self):
        return '{0}'.format(self.values)


def use(values):
    global _settings
    _settings = values


def get_settings():
    global _settings
    return _settings


_settings = Settings()
