# post-it-note django 
Web application for storing notes

## Setup
#### Install requirements:
    pip install -r requirements.txt
#### Perform database migration:
    cd note_manager/
    python manage.py migrate
#### Create superuser:
    python manage.py createsuperuser   
#### Run tests
    python manage.py test
## Run Development Server
    python manage.py runserver

Public endpoint is at http://localhost:8000/note/

Admin endpoint is at http://localhost:8000/admin/
