#!/usr/bin/env bash
# Update the package list and install Nginx
sudo apt update && sudo apt install -y nginx

# Create the necessary directories for the web static deployment
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a symbolic link to the test release directory
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Create a test HTML file in the test release directory
cat << EOF > /data/web_static/releases/test/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Nginx Test Page</title>
</head>
<body>
  </body>
<h1>Congratulations! Your Nginx server is working!</h1>
</html>
EOF

# Change the ownership of the /data directory to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Update the Nginx configuration to serve the web static content
sudo sed -i 's/^server\s*{\s*$/server {\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current;\n\t}/' /etc/nginx/sites-available/default

# Check the Nginx configuration for syntax errors
sudo nginx -t

# Restart the Nginx service to apply the new configuration
sudo service nginx restart

