from fabric.api import local


def read_tag(path):
    # Retrive app version from app image dockerfile
    version = local('cat %s/Dockerfile | \
                    grep -e "^LABEL.version" | \
                    cut -d \\" -f 2' %
                    path, capture=True)

    if not version:
        return None

    return version
