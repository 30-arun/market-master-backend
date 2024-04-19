import boto3
from django.conf import settings
from django.conf import settings
from django.core.mail import send_mail
import boto3
from botocore.exceptions import ClientError

def get_dns_record(domain, record_type, hosted_zone_id, client):
    """
    Retrieve a DNS record from AWS Route 53.

    :param domain: str, The domain name of the record to retrieve.
    :param record_type: str, The type of the record (e.g., 'A', 'MX').
    :param hosted_zone_id: str, The ID of the hosted zone containing the record.
    :return: dict or None, The DNS record if found, otherwise None.
    """
    try:
        # Call Route 53 to list resource record sets
        response = client.list_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            StartRecordName=domain,
            StartRecordType=record_type,
            MaxItems='1'
        )
        # Check if the response contains the record sets
        for record_set in response['ResourceRecordSets']:
            if record_set['Name'].strip('.') == domain and record_set['Type'] == record_type:
                return record_set
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None
    return None


def create_domain(domain, ip_address, subdomain=True, previous_domain=False):
    # Your hosted zone ID
    hosted_zone_id = settings.HOSTED_ZONE_ID

    # Create a Boto3 client for Route 53
    client = boto3.client('route53', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    print(client)
    print(hosted_zone_id)
    if subdomain == True:
        if previous_domain:
            previous_record = get_dns_record(previous_domain, 'A', hosted_zone_id, client)
        else:
            previous_record = False
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
        if previous_record: # if record found also add delete Action in changes
            record_set['Changes'].append({
            'Action': 'DELETE',
            'ResourceRecordSet': {
                'Name': previous_domain,
                'Type': 'A',
                'TTL': 300,
                'ResourceRecords': [{'Value': ip_address}]
            }
        })
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
            'sudo', 'certbot', '--nginx', 
            '--non-interactive', '--agree-tos', '--email', 'maskedman9817@gmail.com', 
            '--redirect', '--expand', '--domains', f'*.marketmaster.me,marketmaster.me,{domain},www.{domain}'
        ]
        update_nginx(domain, server_name=True)
        subprocess.run(certbot_cmd, check=True)
        print(f"SSL certificate generated for {domain}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate SSL certificate for {domain}: {e}", file=sys.stderr)
        return None

def update_nginx(domain, server_name=True):
    """
    Update Nginx configuration for a domain using a Bash script.
    """
    try:
        # Paths for SSL certificates generated by Certbot
        ssl_cert = f'/etc/letsencrypt/live/{domain}/fullchain.pem'
        ssl_key = f'/etc/letsencrypt/live/{domain}/privkey.pem'
        config_file = '/home/ubuntu/update_server_name.sh' if server_name else './update_domain_config.sh'

        # Command to run the Bash script
        update_script_cmd = [
            'sudo', config_file, domain, ssl_cert, ssl_key
        ]
        subprocess.run(update_script_cmd, check=True)
        print(f"Nginx configuration updated for {domain}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update Nginx configuration for {domain}: {e}", file=sys.stderr)
        return None


def send_mail_test(email, token='abc'):
    subject = 'Your forget password link'
    message = f'Hi , '
    email_from = settings.EMAIL_SENDER
    recipient_list = [email]
    print(444,email_from,email,token)
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    print(33)
    return True