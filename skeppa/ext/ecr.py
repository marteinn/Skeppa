from __future__ import absolute_import

import imp

from fabric.api import local, run
from fabric.utils import abort

from . import Extension


class Ecr(Extension):
    def register(self):
        try:
            imp.find_module('awscli')
        except ImportError:
            abort('The ecr extension requires the awscli package '
                  '(hint: pip install awscli)')

    def _verify_image(self, image):
        repository = image.get('repository')
        repro_type = repository.get('type', None)
        return repro_type == 'ecr'

    @staticmethod
    def _build_cli_args(values):
        command = ""
        for key in values:
            if not values[key]:
                continue
            command += " --%s=%s" % (key, values[key])

        return command

    def before_push(self, image):
        if not self._verify_image(image):
            return

        repository = image.get('repository')
        release_tag = image.get('tag', 'latest')

        repository_url = repository.get('url')
        region = repository.get('aws_region', 'us-east-1')
        profile = repository.get('aws_local_profile', '')

        self._login(local, image, region=region, profile=profile)

        # Try to delete previous release_tag from ECR
        try:
            registry_id = repository_url.split(".")[0]
            repository_name = repository_url.split("/")[-1]

            delete_args = {
                "region": region,
                "profile": profile
            }

            delete_command = "aws ecr batch-delete-image --registry-id {0} \
                --repository-name {1} \
                --image-ids imageTag={2}".format(registry_id, repository_name,
                                                 release_tag)

            delete_command += self._build_cli_args(delete_args)
            local(delete_command)
        except:
            pass

    def before_deploy(self, image):
        if not self._verify_image(image):
            return

        repository = image.get('repository')
        region = repository.get('aws_region', 'us-east-1')
        profile = repository.get('aws_profile', '')

        self._login(run, image, region=region, profile=profile)

    def _login(self, method, image, region, profile=""):
        # Authenticate with ecr
        auth_args = {
            "region": region,
            "profile": profile
        }

        auth_command = "aws ecr get-login"

        for arg in auth_args:
            if not auth_args[arg]:
                continue

            auth_command += " --%s=%s" % (arg, auth_args[arg])

        method("$(%s)" % auth_command)


extension = Ecr
