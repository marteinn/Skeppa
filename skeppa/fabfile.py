import sys
import os
import yaml
import six
import importlib
from jinja2 import Template

from fabric.api import run
from fabric.decorators import task
from fabric.contrib.files import exists
from fabric.context_managers import cd
from fabric.state import env
from fabric.utils import abort

from api import ping, setup, build, deploy, push  # NOQA
import ext


def _create_stage(name, stage_config):
    def stage_wrap(*args, **kwargs):
        for key, value in stage_config.iteritems():
            setattr(env, key, value)

        env.exists = exists
        env.run = run
        env.cd = cd

    stage_wrap.__name__ = name
    return task(stage_wrap)


def _load_config(config_path):
    current_dir = os.getcwd()
    config_file = os.path.join(current_dir, config_path)

    with open(config_file, 'r') as stream:
        config_yaml = stream.read()

    config_yaml = Template(config_yaml).render(**env)
    config = yaml.load(config_yaml)

    return config


def _create_stages(stages):
    for name in stages:
        stage = stages[name]
        stage = _normalize_config(stage)

        module_obj = sys.modules[__name__]
        setattr(module_obj, name, _create_stage(name, stage))


def _normalize_config(config):
    for key, value in config.iteritems():
        if key == 'host' and isinstance(value, six.string_types):
            value = [value]

        if key == 'compose_files' and isinstance(value, six.string_types):
            value = [value]

        if key == 'env_files' and isinstance(value, six.string_types):
            value = [value]

        config[key] = value

    return config


if __name__ == 'fabfile':
    config_path = 'skeppa.yml'
    if not os.path.exists(config_path):
        abort('Config file {0} was not found'.format(config_path))

    config = _load_config(config_path)
    extensions = config.pop('extensions', [])

    for ext_name in extensions:
        extension = importlib.import_module('ext.{0}'.format(ext_name))

        ext.register(extension.extension)

    _create_stages(config)
