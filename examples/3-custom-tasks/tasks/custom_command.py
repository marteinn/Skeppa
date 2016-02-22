from fabric.api import task
from fabric.state import env
from fabric.utils import puts


@task
def do_thing():
    """
    Runs a full import
    """
    env.run("docker exec web python /app/manage.py command")
    puts("Command done!")
