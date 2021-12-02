from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from doclib.serializers import DocSerializer
import json
from django.http import JsonResponse
from doclib.models import fileDoc
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from doclib.scripts import google_drive_gcs, awsS3
import requests, os
from django.conf import settings

###################

'''
Parameters for Credentials for configuration
'''
base_dir = settings.BASE_DIR
media_dir = settings.MEDIA_ROOT

storage_chosen = None   # to know the storage service, user selected

bucket_received=None    # to know the bucket of storage service selected
object_token=None       # to know the path in storage service where docs to be uploaded

access_id_received=None
secret_key_received=None

gcs_client_json_file_name=None

###################

def index(request):
    '''
    view for home page of the app, where user
    is provided with the choice of storage service
    selection.
    '''
    return render(request,'storage_service.html')

class get_gcs_credentials(APIView):
    '''
    view for getting credentials of google cloud bucket,
    if user has selected it as a storage service.
    '''
    def get(self, request):
        # rendering HTML Form Page for getting credentials of google cloud bucket
        return render(request, "gcs.html")

    def post(self, request):
        try:
            globals()['bucket_received'] = request.POST.get('bucket')
            globals()['object_token'] = request.POST.get('object_token')
            f = request.FILES.get("files")
            fs = FileSystemStorage()
            file = fs.save(f.name, f)
            # saving the gcs bucket credentials file locally in media directory of the project
            globals()["gcs_client_json_file_name"] = file
            globals()["storage_chosen"] = "gcs"
            # redirecting to files display page
            return redirect("/doclib/files_display")
            
        except Exception as e:
            return "error"

class get_s3_credentials(APIView):
    '''
    view for getting credentials for accessing amazon s3 bucket,
    if user has selected it as a storage service.
    '''
    def get(self, request):
        # rendering HTML Form Page for getting credentials of amazon s3 bucket
        return render(request, "aws_s3.html")
        
    def post(self, request):
        try:
            globals()['bucket_received'] = request.POST.get('bucket')
            globals()['access_id_received'] = request.POST.get('access_id')
            globals()['secret_key_received'] = request.POST.get('secret_key')
            globals()['object_token'] = request.POST.get('object_token')
            globals()["storage_chosen"] = "s3"
            # redirecting to files display page
            return redirect("/doclib/files_display")
            
        except Exception as e:
            print(e)

@csrf_exempt
def google_api(request):
    '''
    view for getting files from Google drive (if user
    has selected it as a data source) and
    saving it locally as an intermediate stage.
    For more details view scripts/google_drive_gcs.py
    '''
    file_details = json.loads(request.body)
    # getting metadata of selected files
    google_drive_gcs.googleAPI().locally_download_files(file_details)
    # calling using google drive service to download selected files
    serializer=DocSerializer(data=file_details,many=True)
    if serializer.is_valid():
        serializer.save()
        # saving metadata of selected files in models
    return JsonResponse({"status": "Success"})

@csrf_exempt
def fetch_credentials_gcs(request):
    '''
    view for getting google API access credentials of
    the client for accessing API services of google,
    particularly google picker and drive api.
    '''
    data = {}
    data["developerKey"] = settings.DEVELOPER_KEY
    data["clientId"] = settings.CLIENT_ID
    data["appId"] = settings.APP_ID
    # sending google API client credentials received from environment variables to google_picker.js in json format
    return JsonResponse(data)

class local_api(APIView):
    '''
    view for uploading files from local storage
    if user has selected it as a data source
    '''
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        form = DocSerializer()
        return render(request, 'local_source.html')
        # rendering HTML Form Page for uploading local files

    def post(self, request, *args, **kwargs):
        all_local_files = []
        fs = FileSystemStorage()

        for f in request.FILES.getlist("files"):
            file = fs.save(f.name,f)
            temp = {"name":file,"url":"local_storage","size":fs.size(file)}
            all_local_files.append(temp)

        file_serializer = DocSerializer(data=all_local_files, many=True)
        if file_serializer.is_valid():
            file_serializer.save()
            # saving metadata of selected files in models
            return redirect("/doclib/files_display")
            # rendering HTML Page for displaying selected files
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class login_dm(APIView):
    '''
    view for signing in the digimocker user account
    '''
    def get(self, request):
        # rendering HTML Form Page for user to login digimocker
        return render(request,'login_digimocker.html')

    def post(self, request):
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        query = {'email':user_email, 'password':user_password}
        # making a login POST request to digimocker api
        response = requests.post('https://digimocker.herokuapp.com/api/user/login', json=query)

        if response.status_code != 200:
            return HttpResponse(status=response.status_code)
        authToken = str(response.text)
        # setting auth-token on successful user login to digimocker
        request.session['token'] = authToken
        request.session['email'] = user_email
        my_headers = {"auth-token": authToken}
        response = requests.post('https://digimocker.herokuapp.com/api/docs', json={"email":user_email},headers=my_headers)
        # making a GET request to digimocker api documents
        
        if response.status_code != 200:
            return HttpResponse(status=response.status_code)
        data=[]
        if(response.text):
            data=json.loads(response.text)
            for jobj in data:
                jobj['fid'] = jobj.pop('_id')
        # rendering HTML Page for displaying user's digimocker files
        return render(request,'showDigimockerFiles.html',{'files':data})
        
class register_dm(APIView):
    '''
    view for registering as a new user in digimocker
    '''
    def get(self, request):
        # rendering HTML Form Page for user to register digimocker
        return render(request,'register_digimocker.html')

    def post(self, request):
        user_name=request.POST.get('name')
        user_email=request.POST.get('email')
        user_password=request.POST.get('password')
        query = {"name":user_name,"email":user_email, "password":user_password}
        response = requests.post('https://digimocker.herokuapp.com/api/user/register', json=query)
        # making a login POST request to digimocker api
        
        if response.status_code != 200:
            return HttpResponse(status=response.status_code)
        # rendering HTML Form Page for user to login digimocker on successful register
        return redirect("/doclib/login_digimocker")

class upload_to_dm(APIView):
    '''
    view for uploading documents to user's digimocker account
    '''
    def get(self, request):
        # rendering HTML Form Page for user to upload new doc to digimocker
        return render(request,'uploadToDm.html')
        
    def post(self, request):
        my_headers = {'auth-token' : request.session['token']}
        # receiving auth-token from session variable
        user_email=request.POST.get('email')
        name=request.POST.get('name')
        email=request.POST.get('email')
        identifier=request.POST.get('identifier')
        url=request.POST.get('url')

        file_data={"name":name,"email":email,"identifier":identifier,"url":url}
        response = requests.post('https://digimocker.herokuapp.com/api/add', json=file_data,headers=my_headers)
        # making a POST request to digimocker api for uploading new doc

        response = requests.post('https://digimocker.herokuapp.com/api/docs', json={"email":user_email},headers=my_headers)
        # making a GET request to digimocker api documents

        data=json.loads(response.text)
        # rendering HTML Page for displaying user's digimocker files
        return render(request,'showDigimockerFiles.html',{'files':data})

class upload_from_dm(APIView):
    '''
    view for selecting documents from user's digimocker account
    if user has selected digimocker as a data source
    '''
    def post(self, request):
        # getting digimocker selected files metadata from checkbox response
        selected_files=request.POST.getlist('selected')
        
        data = []
        for i in range(0,len(selected_files)):
            file_name, file_url = selected_files[i].split(", ")
            r = requests.get(file_url)
            # getting file using downloadable url received in file's metadata

            path = os.path.join(media_dir,str(file_name))
            with open(path,'wb') as f:
                f.write(r.content)
            s = os.stat(path).st_size
            temp = {"name":file_name,"size":s,"url":file_url}
            data.append(temp)
        serializer=DocSerializer(data=data, many=True)
        if serializer.is_valid():
            # saving metadata of selected files in models
            serializer.save()
            # redirecting to files display page
            return redirect("/doclib/files_display")
            
def render_files(request):
    '''
    view for displaying selected files from various
    data sources to the user for final upload with
    an option to delete any file as per requirement
    '''
    # getting files metadata from models, sequenced in reverse order of their size
    files_obj=fileDoc.objects.all().order_by('-size')
    
    # rendering to files display page
    return render(request,'source_display.html',{'files':files_obj})
    

def delete_file(request, id):
    '''
    view for deleting a file ,among
    the list of selected files for upload
    '''
    item = fileDoc.objects.get(pk=id)
    path = os.path.join(media_dir, str(item))
    os.remove(path)
    # deleting selected file from model as well as project local storage i.e. media (here)
    item.delete()

    # rendering to files display page
    return redirect("/doclib/files_display")
    
def clear_user_data_from_app():
    '''
    clearing the files from database as well
    as temporary project storage, either after
    successful upload or if session gets terminated
    '''
    files = fileDoc.objects.all()
    # Retrieving all file's metadata from models
    for file in files:
        os.remove(os.path.join(media_dir,file.name))

    if(globals()['storage_chosen'] == "gcs"):
        os.remove(os.path.join(media_dir, globals()['gcs_client_json_file_name']))
    # Removing the files from project local storage

    for item in os.listdir(media_dir):
        if item.endswith(".json"):
            os.remove(os.path.join(media_dir, item))
    # Removing the files from models
    files.delete()
    globals()['bucket_received'] = None
    globals()['access_id_received'] = None
    globals()['secret_key_received'] = None
    globals()['object_token'] = None
    globals()['storage_chosen'] = None
    globals()['gcs_client_json_file_name'] = None


def upload_S3(request):
    '''
    view for uploading selected documents to amazon s3 bucket
    '''
    # getting files metadata from models, sequenced in reverse order of their size
    files_obj=fileDoc.objects.all().order_by('-size')
    
    if(not len(files_obj)>0):
        return "error"
    info = {}
    info['bucket_received'] = globals()['bucket_received']
    info['object_token'] = globals()['object_token']
    info['access_id_received'] = globals()['access_id_received']
    info['secret_key_received'] = globals()['secret_key_received']
    # uploading files to amazon s3 bucket with access information provided earlier
    return awsS3.upload(files_obj, info)

def upload_gcs(request):
    '''
    view for uploading selected documents to google cloud bucket
    '''
    # getting files metadata from models, sequenced in reverse order of their size
    files_obj = fileDoc.objects.all().order_by('-size')

    if(not len(files_obj)>0):
        return "error"
    info = {}
    info['bucket_received'] = globals()['bucket_received']
    info['object_token'] = globals()['object_token']
    info['gcs_client_json_file_name'] = globals()['gcs_client_json_file_name']
    # uploading files to amazon gcs bucket with access information provided earlier
    return google_drive_gcs.upload(files_obj, info)
    
def upload(request):
    '''
    view for conditional selection of
    storage service based on storage service choosen
    earlier and calling the corresponding upload function
    '''
    storage = globals()['storage_chosen']
    result=[]
    if(storage=="gcs"):
        result = upload_gcs(request)
    elif(storage=="s3"):
        result  = upload_S3(request)

    if(len(result)==0):
        # no files selected by user or session gets terminated
        clear_user_data_from_app()
        return render(request,'errors_page.html',{'error':'session out'})

    elif(result[0]==True):
        # files get successfully uploaded
        clear_user_data_from_app()
        return render(request,"storage_service.html",{'message':True})
    else:
        # error occured while uploading
        clear_user_data_from_app()
        return render(request,'errors_page.html',{'error':result[1],'credentials_error':True})
