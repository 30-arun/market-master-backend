#!/bin/bash

# Check if the correct number of arguments was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

# Arguments
DOMAIN=$1

# Paths
CONFIG_FILE="/etc/nginx/sites-available/market-master"
BACKUP_FILE="/etc/nginx/sites-available/market-master.backup"
DATE=$(date +%Y%m%d%H%M)





# Update or Create Nginx Configuration
update_nginx_config() {
        # Backup the original configuration
        cp $CONFIG_FILE $BACKUP_FILE-$DATE
        # Update existing file
        sed -i "s|^[[:space:]]*\(server_name[[:space:]]*.*\);|\1 $DOMAIN www.$DOMAIN;|g" $CONFIG_FILE
}

# Call function to update Nginx configuration
update_nginx_config

# Test Nginx configuration and reload if no errors
nginx -t && nginx -s reload
