#!/usr/bin/python3
from celery import shared_task
from django.conf import settings
from shared.aws_config.s3 import s3

""" uploads image to s3 """

@shared_task(bind=True, name='delete_duplicate_file')
def delete_old_file(self, oldKey, bucket='trackerr-bucket'):
    try:
        res = s3.delete_object(Bucket=bucket, Key=oldKey)
        print('Deleted: ', oldKey)
        return(0) #res
    except Exception as e:
        raise e
        return {"error": str(e)}
