from fabric.api import task
from fabric.state import env
from fabric.utils import puts


@task
def backup_db():
    """
    Performs a database backup and saves file to /shared/muteparrot_db.sql
    """
    env.run("docker exec container pg_dump -U postgres example_db "
            "-f /shared/example.sql")
    puts("Backup done!")
