# Skeppa

A deployment tool based on docker-compose and fabric. Work in progress.


## Installation

### Develop

    pip install git+git://github.com/marteinn/skeppa.git@develop



## Getting started

First off, head to your project folder to install skeppa.

1. First cd to folder: `cd ~/projects/myproject/`
1. Then setup a virtualenv called venv in your project folder: `virtualenv venv`
1. Activate the environment: `source venv/bin/activate`
1. Now time to install fabrik: `pip install skeppa`

Skeppa is now installed, time to create the `skeppa.yml` file. This file will contain all the deployment instructions you'll need.

1. `touch skeppa.yaml`
2. In your skeppa.yaml, add the following:

    ```yaml
    extensions:
        - ecr
    prod:
        project: hello1
        hosts: ssh.yourhost.com
        user:  ssh-user
        path: /home/youruser/yourproject/
        forward_agent: true
        key_filename: ~/.ssh/id_rsa.pub
        image:
            tag: latest
            name: django-test
            path: src
            repository:
                type: ecr
                aws_region: us-east-1
                url: 999999999.dkr.ecr.us-east-1.amazonaws.com/docker-image
        compose_files: docker-compose-prod.yml
    ```

    This example uses aws-erc as a repository for your image (django-test)


## Usage

- Run a test command against the prod environment

    `skeppa prod ping`


## TODO:
- [x] Handle aws dependency for ecr extension
- [ ] Add image cleanup for ecr extension
- [x] Find out the best way to create a 'pluggable' extension system
- [ ] Publish on pip


## Credits
- http://www.asktherelic.com/2011/02/17/dynamic-fabric-commands-for-managing-cloud-servers/
- http://www.saltycrane.com/blog/2010/09/class-based-fabric-scripts-metaprogramming-hack/


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Skeppa is released under the [MIT License](http://www.opensource.org/licenses/MIT).
