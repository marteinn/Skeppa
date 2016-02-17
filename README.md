# Skeppa

A docker deployment tool built in python. It is based on [fabric](http://www.fabfile.org/) and uses docker-compose to orchestrate and manage containers.


## Requirements

To install Skeppa you need Python 2.7, docker and docker-compose.


## Installation

### Stable

    pip install skeppa

### Develop

    pip install git+git://github.com/marteinn/skeppa.git@develop


## Getting started

First off, head to your project and install skeppa: `pip install skeppa`.

Time to setup deployment instructions. This simple example below will try to build a image called app, push to registry, then deploy on remote machine using the docker-compose file `docker-compose-prod.yml`

1. `touch skeppa.yaml`
2. In your skeppa.yaml, add the following:

    ```yaml
    prod:
        project: test-project
        hosts: ssh.yourhost.com
        user:  ssh-user
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

3. Now run `skeppa prod setup`, this will upload `docker-compose-prod.yml` to your prod path.
4. Time to build and push your docker image, `skeppa prod build deploy`
5. Now when the image has been built and is in your repository, type `skeppa prod deploy` to deploy the image on your remote machine.
6. Done!

Want more [examples](https://github.com/marteinn/Skeppa/tree/develop/examples/)?

## FAQ

- How can I supply env-variables to skeppa?
    - Since skappa is based on fabric just add `-c yourfile.env` when running your command. Skeppa will by default try load either skeppa.env, fabricrc.txt or .fabricrc from your cwd.

- How can I include env-variables in my `skeppa.yaml`?
    - Just define your variables like this `{{ MY_VAR }}`. Example: `host: {{ HOST }}`.


## Usage

The tool consists of 4 commands, they can run in conjunction with eachother.

|Command|Description|Example|
|----------|-------------|-------------|
|setup|Initializes you application by creating the necessary directories/files. Must run first|`skeppa <environment> setup`|
|build|Builds docker images specified in config|`skeppa <environment> build`|
|push|Pushes docker image to registry|`skeppa <environment> push`|
|deploy|Pulls down docker image on remote and runs `docker-compose up`|`skeppa <environment> deploy`|


## Skeppa?

The name is a wordplay with the swedish word for ship = skeppa.


## TODO:
- [x] Handle aws dependency for ecr extension
- [ ] Add image cleanup for ecr extension
- [x] Find out the best way to create a 'pluggable' extension system
- [ ] Publish on pip
- [ ] Add the option to specify your own config
- [x] Add autoload for the config file skepparc.txt
- [x] Rename fabfile to main
- [ ] Add annotated skeppa.yaml
- [ ] Add tests


## Credits/refefences

- [Dynamic Fabric Commands For Managing Cloud Servers](http://www.asktherelic.com/2011/02/17/dynamic-fabric-commands-for-managing-cloud-servers/)
- [Class-based Fabric scripts via a Python metaprogramming hack](http://www.saltycrane.com/blog/2010/09/class-based-fabric-scripts-metaprogramming-hack/)


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Skeppa is released under the [MIT License](http://www.opensource.org/licenses/MIT).
