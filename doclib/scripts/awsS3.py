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

# import boto3
# import os
# import sys
# import threading
# AWS_ACCESS_KEY_ID = "#"

# AWS_SECRET_ACCESS_KEY = '#'
# # session = boto3.Session(
# #     aws_access_key_id=AWS_ACCESS_KEY_ID,
# #     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
# # )
# print(os.getcwd())
# file_path = 't.py'
# bucket = 'bucket1606'
# class ProgressPercentage(object):

#     def __init__(self, filename):
#         self._filename = filename
#         self._size = float(os.path.getsize(filename))
#         self._seen_so_far = 0
#         self._lock = threading.Lock()

#     def __call__(self, bytes_amount):
#         # To simplify, assume this is hooked up to a single filename
#         with self._lock:
#             self._seen_so_far += bytes_amount
#             percentage = (self._seen_so_far / self._size) * 100
#             sys.stdout.write(
#                 "\r%s  %s / %s  (%.2f%%)" % (
#                     self._filename, self._seen_so_far, self._size,
#                     percentage))
#             sys.stdout.flush()
# client = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# )
# response = client.upload_file(file_path, bucket, file_path,Callback=ProgressPercentage(file_path))
# print(response)
