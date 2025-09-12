from os import environ
import boto3

SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
ACCOUNT_ID=environ.get('ACCOUNT_ID')
ENDPOINT_URL=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"



s3 = boto3.client(
        service_name='s3',
        endpoint_url=ENDPOINT_URL,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        aws_access_key_id=ACCESS_KEY_ID
        )
