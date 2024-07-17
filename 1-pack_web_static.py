#!/usr/bin/python3

"""
Script to package the web_static directory into a compressed archive.

This script uses Fabric to run local commands for creating a timestamped
archive of the web_static directory inside a 'versions' directory.

Dependencies:
- Fabric (Install using: pip install fabric)

Usage:
Run this script to create a compressed archive of the web_static directory.
The archive will be saved in the 'versions' directory with a timestamped name.
"""

from datetime import datetime

from fabric.api import local, task


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
