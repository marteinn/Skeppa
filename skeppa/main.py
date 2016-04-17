import importlib
import os
import sys

import six
import yaml
from fabric.api import run
from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.decorators import task
from fabric.state import env
from fabric.utils import abort
from jinja2 import Template

import ext
import settings as skeppa_settings
from api import build, deploy, ping, push, setup  # NOQA


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

        if not isinstance(stage, dict):
            abort('"{0}" is not a valid environment/stage'.format(name))

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


def _load_custom_tasks(tasks):
    sys.path.append(os.getcwd())

    for task_path in tasks:
        name = task_path.split(".")[-1]
        try:
            globals()[name] = importlib.import_module(task_path)
        except ImportError as e:  # NOQA
            abort('Task "{0}" not found'.format(task_path))


if __name__ == 'main':
    # Load configuration
    search_files = ['skeppa.yml', 'skeppa.yaml']
    config_path = None

    # Check if custom skeppa config is present
    try:
        param_index = sys.argv.index('-skeppaconfig')
    except ValueError as e:
        param_index = -1

    if param_index != -1 and len(sys.argv) > param_index+1:
        search_files = [sys.argv[param_index+1]]

    # Make sure config exist in io
    for path in search_files:
        if os.path.exists(path):
            config_path = path
            break

    if not config_path:
        abort('Config file {0} was not found'.format(search_files[0]))

    config = _load_config(config_path)

    # Manage settings
    settings_data = config.pop('settings', {})

    instance = skeppa_settings.Settings(values=settings_data)
    skeppa_settings.use(instance)

    settings = skeppa_settings.get_settings()

    # Activate extensions
    for ext_name in settings.extensions:
        extension = importlib.import_module('ext.{0}'.format(ext_name))
        ext.register(extension.extension)

    # Load any extra tasks
    _load_custom_tasks(settings.tasks)

    # Create stages
    _create_stages(config)
