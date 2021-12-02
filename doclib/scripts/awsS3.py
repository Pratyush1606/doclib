import os
import boto3
from django.conf import settings

base_dir = settings.BASE_DIR
media_dir = settings.MEDIA_ROOT

def upload(files_obj, info):
    uploaded_error = ""
    uploaded_check = False
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=info['access_id_received'],
            aws_secret_access_key=info['secret_key_received']
        )
        bucket_name = info['bucket_received']
        object_name = info['object_token']

        if(object_name != ""):   # whether a specific s3 path is given by the user
            object_name += "/"

        for file in files_obj:
            client.upload_file(os.path.join(media_dir,file.name), bucket_name, object_name+file.name)
        uploaded_check = True
    except boto3.exceptions.Boto3Error as e:
        uploaded_error = e

    return [uploaded_check,uploaded_error]
