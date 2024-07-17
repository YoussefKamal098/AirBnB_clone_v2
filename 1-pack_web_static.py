#!/usr/bin/python3
"""
Script to package the web_static directory into a compressed archive.

This script uses Fabric to run local commands for creating a timestamped
archive of the web_static directory inside a 'versions' directory.

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
    fab -f ./path/to/fabfile do_pack
"""

import os
from datetime import datetime

from fabric.api import local, task


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
