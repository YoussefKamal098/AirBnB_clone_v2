# Update the package list and install Nginx
package { 'nginx':
  ensure => installed,
  before => Service['nginx'],
}

# Ensure the necessary directories are present
file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
  before => File['/data/web_static/shared'],
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create the test HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Nginx Test Page</title>
    </head>
    <body>
      <h1>Congratulations! Your Nginx server is working!</h1>
    </body>
    </html>
',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Ensure the ownership of the /data directory
file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# # Update the Nginx configuration to serve the web static content
# file { '/etc/nginx/sites-available/default':
#   ensure  => file,
#   mode    => '0644',
#   content => template('nginx/default.erb'),
#   notify  => Service['nginx'],
# }

# Update the Nginx configuration to serve the web static content using sed command
exec { 'update_nginx_config':
  command =>
    'sudo sed -i \'s/^server\s*{\s*$/server {\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current;\n\t}/\' /etc/nginx/sites-available/default'
  ,
  onlyif  => 'test ! $(grep -q "location /hbnb_static" /etc/nginx/sites-available/default)',
  notify  => Service['nginx'],
}

# Ensure the Nginx service is running
service { 'nginx':
  ensure => running,
  enable => true,
}

# Template for the Nginx configuration
# Create a file named 'default.erb' in a templates directory in your module
# with the following content:
#
# server {
#   location /hbnb_static {
#     alias /data/web_static/current;
#   }
#   ...
# }
#
# Make sure to include other necessary server configuration in the template.
