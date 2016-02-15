from __future__ import absolute_import

from . import Extension
from fabric.api import env, local, run


class Ecr(Extension):
    def register(self):
        pass

    def _verify_image(self, image):
        repository = image.get('repository')
        repro_type = repository.get('type', None)
        return repro_type == 'ecr'

    def before_push(self, image):
        if not self._verify_image(image):
            return

        repository = image.get('repository')
        region = repository.get('aws_region', 'us-east-1')
        profile = repository.get('aws_local_profile', '')

        self._login(local, image, region=region, profile=profile)

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

        print(auth_command)
        method("$(%s)" % auth_command)
