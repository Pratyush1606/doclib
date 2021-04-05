import os
import io
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import storage, exceptions
from google.oauth2 import service_account
from django.conf import settings

SCOPES = "https://www.googleapis.com/auth/drive.file"
base_dir=settings.BASE_DIR
media_dir = settings.MEDIA_ROOT
CLIENT_SECRET_FILE = os.path.join(base_dir,"credentials_dir/credentials_gcs.json")

class googleAPI:
    def __init__(self):
        self.client_secret = CLIENT_SECRET_FILE
        self.scopes = SCOPES
        self.creds = None

    def get_credentials(self):
        """
        For getting the credentials (say accessToken) of the user
        """
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secret, self.scopes)
        self.creds = flow.run_local_server(port=8080)

    def get_drive_service(self):
        """
        For getting the drive_service instance from
        the credentials of the user
        """
        self.get_credentials()
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def check_name(self, file):
        file_name = file['name']
        last_dot_ind = -1
        for i in range(len(file_name)-1,-1,-1):
            if(file_name[i]=="."):
                last_dot_ind = i
                break
        if(os.path.exists(os.path.join(media_dir, file_name))):
            file_name = file_name[:last_dot_ind] + "_" + file["file_id"] + file_name[last_dot_ind:]
            file["name"] = file_name

    def locally_download_files(self, fileList,dm=False):
        """
        For locally downloading the files
        """
        self.get_drive_service()

        for file in fileList:
            if dm==True:
                media_request = self.drive_service.files().get(fileId=file['file_id'])
            else:
                media_request = self.drive_service.files().get_media(fileId=file['file_id'])
            print(media_request)
            self.check_name(file)
            fh = io.FileIO(os.path.join(media_dir, file['name']), 'wb')
            downloader = MediaIoBaseDownload(fh, media_request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %s, %d%%"%(file['name'],int(status.progress() * 100)))


def upload(files_obj, info):
    uploaded_check = False
    uploaded_error = ""
    try:
        bucket_name = info['bucket_received']
        object_name = info['object_token']
        credentials = service_account.Credentials.from_service_account_file(os.path.join(media_dir, info['gcs_client_json_file_name']))
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.get_bucket(bucket_name)

        if(object_name!=""):
            object_name += "/"

        for file in files_obj:
            blob = bucket.blob(object_name+file.name)
            blob.upload_from_filename(os.path.join(media_dir, file.name))

        uploaded_check = True

    except Exception as e:
        uploaded_error = e

    return [uploaded_check, uploaded_error]
