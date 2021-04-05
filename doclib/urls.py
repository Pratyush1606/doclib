from django.urls import path
from doclib import views
from django.conf import settings # new

app_name='doclib'
urlpatterns=[

    path('',views.index,name='selectSS'),
    path('fetch_cred_gcs',views.fetch_credentials_gcs,name="fetch_cred_gcs"),
    path('storage_source/awsS3', views.get_s3_credentials.as_view(), name='awsS3'),
    path('storage_source/gcs', views.get_gcs_credentials.as_view(), name="gcs"),
    path('google_api', views.google_api, name="g_api"),
    path('files_display', views.render_files, name="display_Files"),
    path('file_delete/<id>', views.delete_file, name='deleteFile'),
    path('local_api', views.local_api.as_view(), name="local_api"),
    path('upload', views.upload, name="upload"),
    path('login_digimocker',views.login_dm.as_view(),name="login_Digimocker"),
    path('register_digimocker',views.register_dm.as_view(),name="register_Digimocker"),
    path('upload_to_digimocker',views.upload_to_dm.as_view(),name="upload_To_Digimocker"),
    path('upload_from_digimocker',views.upload_from_dm.as_view(),name="upload_From_Digimocker"),
]
