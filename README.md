# post-it-note_django
Web application for storing notes

## Setup
### Install Django:
    pip install Django==3.0.2
### Perform database migration:
    cd note_manager/
    python manage.py check
    python manage.py migrate
### Create superuser:
    python manage.py createsuperuser
## Run Development Server
    python manage.py runserver

Public endpoint is at http://localhost:8000/note/

Admin endpoint is at http://localhost:8000/admin/
