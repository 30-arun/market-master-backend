#!/bin/bash

# Check if the correct number of arguments was provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <domain> <ssl_certificate_path> <ssl_key_path>"
    exit 1
fi

# Arguments
DOMAIN=$1
SSL_CERT=$2
SSL_KEY=$3

# Paths
CONFIG_FILE="/etc/nginx/sites-available/$DOMAIN"
BACKUP_FILE="/etc/nginx/sites-available/$DOMAIN.backup"
DATE=$(date +%Y%m%d%H%M)

# Backup the original configuration
cp $CONFIG_FILE $BACKUP_FILE-$DATE

# Update or Create Nginx Configuration
update_nginx_config() {
    # Check if the config file exists, if not create a basic structure
    if [ ! -f "$CONFIG_FILE" ]; then
        cat <<EOF > "$CONFIG_FILE"
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    ssl_certificate $SSL_CERT;
    ssl_certificate_key $SSL_KEY;

    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        include proxy_params;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/ubuntu/market-master-frontend/out/;
        access_log off;
    }
    location /media/ {
        root /home/ubuntu/market-master-backend/;
    }
    location /logos/ {
        root /home/ubuntu/market-master-frontend/out/;
    }
}
EOF
    else
        # Update existing file
        sed -i "" "s|^[[:space:]]*\(server_name[[:space:]]*.*\);|\1 $DOMAIN www.$DOMAIN;|g" $CONFIG_FILE
    fi
}

# Call function to update Nginx configuration
update_nginx_config

# Test Nginx configuration and reload if no errors
nginx -t && nginx -s reload
