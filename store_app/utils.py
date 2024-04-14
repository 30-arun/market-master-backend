import boto3
from django.conf import settings

def create_subdomain(subdomain, ip_address):
    # Your hosted zone ID
    hosted_zone_id = settings.HOSTED_ZONE_ID

    # Create a Boto3 client for Route 53
    client = boto3.client('route53', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    print(client)
    print(hosted_zone_id)
    # Define the DNS record to create
    record_set = {
        "Comment": "Automatic DNS update",
        'Changes': [
            {
                'Action': 'UPSERT',  # "UPSERT" will either create or update the record
                'ResourceRecordSet': {
                    'Name': subdomain,
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
        print(f"Failed to create subdomain: {e}")
        return None

