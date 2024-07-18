#!/usr/bin/python3
"""
Fabric script to clean up old versions of web_static releases.

This script connects to remote web servers and removes outdated
versions of web_static archives, keeping only the most recent ones.

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
1. Set the remote server information in the env variables.
2. Run the script using:
   fab -f ./path/to/this/script do_clean:number=<number_of_versions_to_keep> \
   -u <username-on-remote-server> \
   -i <path-to-public-key>

Note:
Replace 'web-01.realyousam.tech' and 'web-02.realyousam.tech' with the actual
hostnames or IP addresses of your web servers.
"""

from fabric.api import local, task, sudo, lcd, cd, env

# Define the hosts to connect to
env.hosts = ["web-01.realyousam.tech", "web-02.realyousam.tech"]


# Uncomment and set the following lines with your server's
#   username and path to SSH key if needed
# env.user = "username"  # replace with your username of the remote server
# env.key_filename = "/path/to/public/key eg. ~/.ssh/id_rsa"


@task
def do_clean(number=0):
    """
    Deletes out-of-date archives, keeping only the specified
    number of recent ones.

    Args:
    - number: The number of recent archives to keep. If 0,
        keeps only the most recent archive.

    This function performs the following steps:
        1. Converts the number argument to an integer.
        2. If number is 0, sets it to 2 to keep the most recent archive.
        3. Deletes older archives locally from the 'versions' directory.
        4. Deletes older archives remotely from the
            '/data/web_static/releases' directory.
    """

    try:
        number = int(number)

        if number == 0:
            number = 2
        else:
            number += 1

        # Clean up old versions locally in the 'versions' directory
        with lcd("versions"):
            local(f"ls -t | tail -n +{number} | xargs rm -rf")

        # Clean up old versions on the remote server in the
        #   '/data/web_static/releases' directory
        with cd("/data/web_static/releases"):
            sudo(f'ls -t | tail -n +{number} | xargs rm -rf')
    except Exception as error:
        print(f"An error occurred during clean up: {error}")
