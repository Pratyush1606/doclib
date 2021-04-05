# DOCLIB

A document library that integrates with multiple data sources (like digiLocker, Google Drive, local storage etc.) and storage services (like S3 and Google Cloud Storage) and uploads data from these data sources to the chosen storage service. It can be integrated with any Django Project.

## **TECHNOLOGIES**

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/): Django builds better web apps with less code
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Rest APIs with Django
* Frontend: HTML5, Bootstrap, JS
* Architecture of the Library
![Architecture](https://drive.google.com/uc?export=view&id=1klItD0DEG-0b9NExLGSS_QUkOwYDNs8v)

## **CURRENT SUPPORTED SERVICES**

### DATA SOURCES

* [Google Drive](https://www.google.com/intl/en_in/drive/)

* Local Storage

* Digimocker (mock of [Digilocker](https://digilocker.gov.in/))

### STORAGE SERVICES

* [Amazon S3](https://aws.amazon.com/s3/)

* [Google Cloud Storage](https://cloud.google.com/storage)

## **QUICKSTART**

Install the package  

```py
pip install django-doclib
```

### Before running the server, make sure ```Directory``` looks like

```
demo_proj
├── credentials_dir
|      └── credentials_gcs.json
├── media
└── django_project_folder
    ├── settings.py
    ├── asgi.py
    ├── .env
    ├── wsgi.py
    └── urls.py
```

### Follow the steps

1. Add ``doclib`` and ``rest_framework`` to your INSTALLED_APPS setting like this

    INSTALLED_APPS = [  
        ...  
        'doclib',  
        'rest_framework',  
    ]

2. Include the doclib URLconf in your project urls.py like this

    ``path('doclib/', include('doclib.urls'))``

3. Provide ``MEDIA_ROOT`` in your project settings.py, something like this

    ``MEDIA_ROOT = os.path.join(BASE_DIR, 'media')``

4. For integrating with Google Drive

    * Make a directory with name ``credentials_dir`` at the project root level

    * Put the google api client secret json file with name as ``credentials_gcs.json`` in ``credentials_dir`` directory
    For getting the API and Developer keys, visit [here](https://cloud.google.com/docs/authentication/production#create_service_account).

    * Make a ``.env`` file in the project folder directory (at the project settings.py level) and put the Browser API keys obtained from the Google API Console like this (don’t use quotations around strings)

        ``DEVELOPER_KEY``=##################  
        ``CLIENT_ID``=##################  
        ``CLIENT_SECRET``=##################  
        ``APP_ID``=##################

5. For setting the environment variables, follow this

    * Add these below lines in the project ``settings.py``

        ```py
        import environ
        env = environ.Env()
        environ.Env.read_env()
        ```

    * For setting the above API Keys put these below lines in the ``settings.py``

        ```py
        DEVELOPER_KEY = env("DEVELOPER_KEY")
        CLIENT_ID     = env("CLIENT_ID")
        CLIENT_SECRET = env("CLIENT_SECRET")
        APP_ID        = env("APP_ID")
        ```

6. Run ``python manage.py migrate`` to create the doclib models.

7. Start the development server and visit ``http://localhost:8000/doclib/`` to access the doclib.

## **REPOSITORY WALKTHROUGH**

### ``doclib``

> Contains the source code of the library  

### ``slicedoc``

> A demo django project using ``doclib`` library

> For using this django project

1. install the library package

2. Clone the repo

3. Change working directory to repo_folder

    ```sh
    cd path/to/repo_folder
    ```

4. Go to ``slicedoc`` folder

    ```sh
    cd slicedoc
    ```

5. Put the google api client secret json file with name as ``credentials_gcs.json`` in ``credentials_dir`` directory

6. Set the Browser API keys obtained from the Google API Console in the ``.env`` file in project directory

7. Run ``python manage.py migrate`` to create the doclib models.

8. Start the development server and visit ``http://localhost:8000/doclib/`` to access the doclib.
