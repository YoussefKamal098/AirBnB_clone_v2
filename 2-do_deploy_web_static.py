#!/usr/bin/python3
"""
Script to distribute an archive to web servers.

This script uses Fabric to create a compressed archive of the web_static
directory and distribute it to specified web servers.

Dependencies:
- Fabric (Install using: pip install fabric )
    $ pip3 uninstall Fabric
    $ sudo apt-get install libffi-dev
    $ sudo apt-get install libssl-dev
    $ sudo apt-get install build-essential
    $ sudo apt-get install python3.4-dev or 3.7-dev
    $ sudo apt-get install libpython3-dev
    $ pip3 install pyparsing
    $ pip3 install appdirs
    $ pip3 install setuptools==40.1.0
    $ pip3 install cryptography==2.8
    $ pip3 install bcrypt==3.1.7
    $ pip3 install PyNaCl==1.3.0
    $ pip3 install Fabric3==1.14.post1

Usage:
1. Create the archive by running:
   fab -f ./path/to/fab/file do_pack

2. Deploy the created archive by running:
   fab -f ./path/to/fab/file deploy_archive:/path/to/archive.tgz \
   -u <username-on-remote-server> \
   -i <path-to-public-key>

Note:
Replace '/path/to/archive.tgz' with the actual path to the archive
created in step 1.
"""
import os

from fabric.api import run, put, env

env.hosts = ["web-01.realyousam.tech", "web-02.realyousam.tech"]


# env.user = "ubuntu"  # replace with your username of the remote server
# env.key_filename = "/path/to/public/key eg. ~/.ssh/id_rsa"


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
