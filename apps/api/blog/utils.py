import boto3
from django.conf import settings
from botocore.exceptions import ClientError
from datetime import timedelta


def generate_signed_url(file_field, expiration=3600):
    """
    Generate a signed URL for an S3 file that allows temporary access
    
    Args:
        file_field: Django FileField or ImageField instance
        expiration: URL expiration time in seconds (default: 1 hour)
    
    Returns:
        str: Signed URL or None if error
    """
    if not file_field or not file_field.name:
        return None
    
    try:
        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=getattr(settings, 'AWS_SESSION_TOKEN', None),
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # Generate signed URL
        signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': file_field.name
            },
            ExpiresIn=expiration
        )
        
        return signed_url
        
    except ClientError as e:
        print(f"Error generating signed URL: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error generating signed URL: {e}")
        return None
