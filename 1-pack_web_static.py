#!/usr/bin/python3

from datetime import datetime

from fabric.api import local, task


@task
def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"web_static_{now}.tgz"
    archive_path = f"versions/{archive_name}"

    try:
        local("mkdir -p versions")
        local(f"tar -cvzf versions/{archive_name} web_static")

        return archive_path
    except Exception:
        return None
