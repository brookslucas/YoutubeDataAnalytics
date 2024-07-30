import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
import os

# Fetching credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


def upload_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload 
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used as object_name
    :return: True if file was uploaded, else False
    """
   # Creating an S3 client with credentials from environment variables
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    try:
        # Uploading the file
        response = s3_client.upload_file(file_name, bucket, object_name)
        logging.info(f"File {file_name} uploaded to {bucket} as {object_name}")
    except FileNotFoundError:
        logging.error("The file was not found")
        return False
    except NoCredentialsError:
        logging.error("Credentials not available")
        return False
    except ClientError as e:
        logging.error(f"Client error: {e}")
        return False

    return True
