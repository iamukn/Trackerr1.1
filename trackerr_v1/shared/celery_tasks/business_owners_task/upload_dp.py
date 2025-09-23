#!/usr/bin/python3
from celery import shared_task
from django.conf import settings
from business.utils import resize_and_upload                                                                                                                 
""" uploads image to s3 """
    
@shared_task(bind=True, name='upload_dp')
def upload_dp(self,file_obj, key, bucket='trackerr-bucket'):
    try:
        res = resize_and_upload.resize_and_upload(file_obj=file_obj, key=key, bucket=bucket)
        return(0) #res
    except Exception as e:
        return {"error": str(e)}
