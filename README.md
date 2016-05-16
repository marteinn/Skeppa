[![PyPI version](https://badge.fury.io/py/skeppa.svg)](https://badge.fury.io/py/skeppa)

# Skeppa

A docker deployment tool built in python. It is based on [fabric](http://www.fabfile.org/) and uses docker-compose to orchestrate and manage containers. You can use it to build images, push images and trigger updates on remote machines.


## Requirements

To install Skeppa you need Python 2.7, docker and docker-compose.


## Installation

### Stable

    pip install skeppa

### Develop

    pip install git+git://github.com/marteinn/skeppa.git@develop


## Getting started

First off, head to your project and install skeppa: `pip install skeppa`.

Time to setup deployment instructions. This simple example below build a image called app, push it to a registry, then deploy on remote machine using the docker-compose file.

1. `touch skeppa.yaml`
2. In your skeppa.yaml, add the following:

    ```yaml
    prod:
        project: test-project
        hosts: ssh.yourhost.com
        user: ssh-user
        path: /home/youruser/yourproject/
        key_filename: ~/.ssh/id_rsa.pub
        image:
            name: app
            path: app
            repository:
                url: registry.mydomain.com/app-image
        compose_files: docker-compose.yml
    ```

    _(This example requires docker image called `app` in your project folder, a working docker repository and a working `docker-compose.yml`)._

    _Want a full annotated [skeppa.yaml](https://github.com/marteinn/Skeppa/blob/develop/skeppa.annotated.yaml)?_



3. Then run `skeppa prod setup`, this will upload `docker-compose.yml` to your prod path.
4. Time to build a docker image of your app `skeppa prod build`
5. Now send the image you just built to your registry `skeppa prod push`
5. Finally type `skeppa prod deploy` to deploy the image on your remote machine and create running containers.
6. Done!

Want more [examples](https://github.com/marteinn/Skeppa/tree/develop/examples/)?


## FAQ

- How can I supply env-variables to skeppa?
    - Since skappa is based on fabric just add `-c yourfile.env` when running your command. Skeppa will by default try load either skeppa.env, fabricrc.txt or .fabricrc from your cwd.

- How can I include env-variables in my `skeppa.yaml`?
    - Just define your variables like this `{{ MY_VAR }}`. Example: `host: {{ HOST }}`.

- Can I define my own custom `skeppa.yaml`, such as `skeppa-prod.yaml`?
    - Sure! Add the argument `-skeppaconfig` in your command, like this: `skeppa prod ping  -skeppaconfig skeppa-prod.yaml`


## Usage

The tool consists of 4 commands, they can run in conjunction with eachother.

|Command|Description|Example|
|----------|-------------|-------------|
|setup|Initializes you application by creating the necessary directories/files. Must run first|`skeppa <environment> setup`|
|build|Builds docker images specified in config|`skeppa <environment> build`|
|push|Pushes docker image to registry|`skeppa <environment> push`|
|deploy|Pulls down docker image on remote and runs `docker-compose up`|`skeppa <environment> deploy`|


## Skeppa?

The name is a wordplay with the swedish word for "to ship" = "skeppa".


## Git hooks

These hooks will automatically bump the application version when using `git flow release ...`

```
ln -nfs $PWD/git-hooks/bump-version.sh .git/hooks/post-flow-release-start
ln -nfs $PWD/git-hooks/bump-version.sh .git/hooks/post-flow-hotfix-start
```


## Credits/references

- [Dynamic Fabric Commands For Managing Cloud Servers](http://www.asktherelic.com/2011/02/17/dynamic-fabric-commands-for-managing-cloud-servers/)
- [Class-based Fabric scripts via a Python metaprogramming hack](http://www.saltycrane.com/blog/2010/09/class-based-fabric-scripts-metaprogramming-hack/)


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Skeppa is released under the [MIT License](http://www.opensource.org/licenses/MIT).
