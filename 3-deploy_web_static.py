#!/usr/bin/python3
"""
Script to automate the deployment of a web application to multiple servers.

This script uses Fabric, a Python library for remote server automation, to:
1. Create an Archive:
   - Compresses the `web_static` directory into a `.tgz` archive.
   - Stores the archive in the `versions` directory.

2. Deploy the Archive:
   - Uploads the created archive to specified web servers.
   - Uncompresses the archive into a designated release directory
        on the remote servers.
   - Updates the symbolic link to point to the new release,
        ensuring the servers serve the latest version.

Dependencies:
- Fabric (Install using: pip install fabric)
    $ pip3 uninstall Fabric
    $ sudo apt-get install libffi-dev
    $ sudo apt-get install libssl-dev
    $ sudo apt-get install build-essential
    $ sudo apt-get install python3.4-dev or python3.7-dev
    $ sudo apt-get install libpython3-dev
    $ pip3 install pyparsing
    $ pip3 install appdirs
    $ pip3 install setuptools==40.1.0
    $ pip3 install cryptography==2.8
    $ pip3 install bcrypt==3.1.7
    $ pip3 install PyNaCl==1.3.0
    $ pip3 install Fabric3==1.14.post1

Usage:
    fab -f ./path/to/fabfile deploy \
   -u <username-on-remote-server> \
   -i <path-to-public-key>

Note:
Replace '<username-on-remote-server>' with your remote server username.
Replace '<path-to-public-key>' with the path to your SSH public key.
"""

import os
from datetime import datetime

from fabric.api import task, local, run, put, env

env.hosts = ["web-01.realyousam.tech", "web-02.realyousam.tech"]


# env.user = "username"  # replace with your username of the remote server
# env.key_filename = "/path/to/public/key eg. ~/.ssh/id_rsa"


@task
def do_pack():
    """
    Creates a compressed archive of the web_static directory.

    Returns:
    - If successful, returns the path to the created archive.
    - If an error occurs during the process, returns None.

    This function performs the following steps:
        1. Generates a timestamp to include in the archive name.
        2. Creates the 'versions' directory if it doesn't exist.
        3. Creates a compressed archive of the 'web_static' directory.
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

        archive_size = os.stat(archive_path).st_size
        print(f"web_static packed: {archive_path} -> {archive_size} Bytes")

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

    This function performs the following steps:
        1. Checks if the archive path exists.
        2. Extracts the archive file name and base name.
        3. Ensures the target directory on the remote server is clean.
        4. Uploads the archive to the remote server.
        5. Uncompresses the archive into the target directory.
        6. Cleans up temporary files and directories.
        7. Updates the symbolic link to point to the new release.
    """
    if not os.path.exists(archive_path):
        print(f"Archive path {archive_path} does not exist.")
        return False

    try:
        # Extract the archive file name and name without extension
        archive_file = os.path.basename(archive_path)
        archive_base_name = os.path.splitext(archive_file)[0]
        remote_tmp_path = f"/tmp/{archive_file}"
        release_dir = f"/data/web_static/releases/{archive_base_name}/"

        # Ensure the target directory is clean
        run(f"sudo rm -rf {release_dir}")
        run(f"sudo mkdir -p {release_dir}")

        # Upload the archive to the remote server
        put(archive_path, remote_tmp_path)

        # Uncompress the archive into the target directory
        run(f"sudo tar -xzf {remote_tmp_path} -C {release_dir}")

        # Clean up the temporary archive file
        run(f"sudo rm {remote_tmp_path}")

        # Move contents out of the nested web_static directory
        run(f"sudo mv {release_dir}/web_static/* {release_dir}")
        run(f"sudo rm -rf {release_dir}/web_static")

        # Update the symbolic link to point to the new release
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {release_dir} /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception as error:
        print(f"An error occurred during deployment: {error}")
        return False


@task
def deploy():
    """
    Automates the full deployment process:
    1. Creates a compressed archive of the web_static directory.
    2. Distributes the created archive to the web servers.

    Returns:
    - bool: True if the deployment was successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
