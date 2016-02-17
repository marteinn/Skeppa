active_extensions = []


class Extension(object):
    def register(self):
        pass


def dispatch(event, *args, **kwargs):
    for extension in active_extensions:
        if not hasattr(extension, event):
            continue

        getattr(extension, event)(*args, **kwargs)


def register(extension):
    instance = extension()
    active_extensions.append(instance)

    instance.register()
