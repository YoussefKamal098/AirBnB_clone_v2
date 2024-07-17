#!/usr/bin/python3
"""
Script to distribute an archive to web servers.
"""

import os
from datetime import datetime

from fabric.api import task, local, sudo, put, env

env.hosts = ["web-01.realyousam.tech", "web-02.realyousam.tech"]


# env.user = "ubuntu" replace with your username of the remote server
# env.key_filename = "/path/to/public/key eg. ~/.ssh/id_rsa"


@task
def do_pack():
    """
    Creates a compressed archive of the web_static directory.

    Returns:
    - If successful, returns the path to the created archive.
    - If an error occurs during the process, returns None.
    """
    try:
        # Generate timestamp
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"web_static_{now}.tgz"
        archive_path = f"versions/{archive_name}"

        # Create 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Create the compressed archive
        local(f"tar -cvzf {archive_path} web_static")

        return archive_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@task
def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
    - archive_path: Path to the archive to distribute.

    Returns:
    - True if the archive was successfully distributed.
    - False if the archive was not distributed.
    """

    if not os.path.exists(archive_path):
        print(f"Archive path {archive_path} does not exist.")
        return False

    try:
        archive_file = os.path.basename(archive_path)
        temp_archive_dir = "/tmp/"
        temp_archive_file = f"/tmp/{archive_file}"
        archive_name = os.path.splitext(archive_file)[0]
        uncompressed_to = f"/data/web_static/releases/{archive_name}/"

        sudo(f"rm -rf {uncompressed_to}")
        sudo(f"mkdir -p {uncompressed_to}")

        put(archive_path, temp_archive_dir)

        sudo(f"tar -xzf {temp_archive_file} -C {uncompressed_to}")
        sudo(f"rm {temp_archive_file}")
        sudo(f"mv {uncompressed_to}/web_static/* {uncompressed_to}")
        sudo(f"rm -rf {uncompressed_to}/web_static")
        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -s {uncompressed_to} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False
