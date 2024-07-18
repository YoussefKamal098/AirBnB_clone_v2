# Puppet manifest to setup web servers for deployment of web_static

# Update package list and install Nginx
exec { 'update_package_list':
  command => '/usr/bin/env apt -y update',
  path    => '/usr/bin:/usr/sbin:/bin:/usr/local/bin',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['update_package_list'],
}

# Ensure directories are present
file { '/data':
  ensure => directory,
}

file { '/data/web_static':
  ensure => directory,
}

file { '/data/web_static/releases':
  ensure => directory,
}

file { '/data/web_static/releases/test':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

# Create test HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <p>Nginx server test</p>
  </body>
</html>',
  require => File['/data/web_static/releases/test'],
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Change ownership of /data directory
exec { 'chown_data_directory':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => '/usr/bin:/usr/local/bin:/bin',
  require => File['/data'],
}

# Ensure /var/www directory exists for Nginx
file { '/var/www':
  ensure => directory,
}

file { '/var/www/html':
  ensure => directory,
}

# Create default index.html for /var/www/html
file { '/var/www/html/index.html':
  ensure  => present,
  content => '<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <p>Nginx server test</p>
  </body>
</html>',
  require => File['/var/www/html'],
}

# Update Nginx configuration
exec { 'nginx_conf':
  command =>
    'sudo sed -i \'s/^server\s*{\s*$/server {\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current;\n\t}/\' /etc/nginx/sites-enabled/default'
  ,
  path    => '/usr/bin:/usr/sbin:/bin:/usr/local/bin',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Exec['nginx_conf'],
}
