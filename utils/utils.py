import boto3
from django.conf import settings

def create_domain(domain, ip_address, subdomain=True):
    # Your hosted zone ID
    hosted_zone_id = settings.HOSTED_ZONE_ID

    # Create a Boto3 client for Route 53
    client = boto3.client('route53', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    print(client)
    print(hosted_zone_id)
    if subdomain == True:
        # Define the DNS record to create
        record_set = {
            "Comment": "Automatic DNS update",
            'Changes': [
                {
                    'Action': 'UPSERT',  # "UPSERT" will either create or update the record
                    'ResourceRecordSet': {
                        'Name': domain,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': ip_address}]
                    }
                }
            ]
        }
    else:
        record_set = {
            "Comment": "Automatic DNS update",
            'Changes': [
                {
                    'Action': 'UPSERT',  # "UPSERT" will either create or update the record
                    'ResourceRecordSet': {
                        'Name': domain,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': ip_address}]
                    }
                },
                {
                    'Action': 'UPSERT',  # "UPSERT" will either create or update the record
                    'ResourceRecordSet': {
                        'Name': f'www.{domain}',
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [{'Value': ip_address}]
                    }
                }
            ]
        }
    # Try to create the subdomain record
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=record_set
        )
        return response
    except Exception as e:
        print(f"Failed to create domain: {e}")
        return None

import subprocess
import sys

def generate_ssl(domain):
    """
    Generate or renew an SSL certificate for a domain using Certbot.
    """
    try:
        # Run Certbot command for generating SSL
        certbot_cmd = [
            'sudo', 'certbot', '--nginx', '-d', domain, '-d', f'www.{domain}', 
            '--non-interactive', '--agree-tos', '--email', 'maskedman9817@gmail.com', 
            '--redirect', '--hsts', '--expand'
        ]
        subprocess.run(certbot_cmd, check=True)
        print(f"SSL certificate generated for {domain}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate SSL certificate for {domain}: {e}", file=sys.stderr)
        return None

def update_nginx(domain):
    """
    Update Nginx configuration for a domain using a Bash script.
    """
    try:
        # Paths for SSL certificates generated by Certbot
        ssl_cert = f'/etc/letsencrypt/live/{domain}/fullchain.pem'
        ssl_key = f'/etc/letsencrypt/live/{domain}/privkey.pem'

        # Command to run the Bash script
        update_script_cmd = [
            'sudo', './update_domain_config.sh', domain, ssl_cert, ssl_key
        ]
        subprocess.run(update_script_cmd, check=True)
        print(f"Nginx configuration updated for {domain}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update Nginx configuration for {domain}: {e}", file=sys.stderr)
        return None

