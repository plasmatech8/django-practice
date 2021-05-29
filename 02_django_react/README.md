# Django & React

See:
* [Django & React Tutorial ](https://www.youtube.com/watch?v=JD-age0BPVo) By Tech With Tim on YouTube
* ...

Contents:
- [Django & React](#django--react)
  - [01. Basics](#01-basics)
    - [Setup](#setup)
    - [Create an app in the project](#create-an-app-in-the-project)
    - [Adding a view](#adding-a-view)

## 01. Basics

### Setup

Environment:
* `requirements.txt`
  * django
  * django rest framework
* Consider using containers/devcontainers
  * `python` container
* Consider using virtual environments
  * `python -m venv env` > Select Interpreter

Add a `.gitignore`

Create a project using tha django-admin command:
```bash
django-admin startproject music_controller
```

Create admin user for admin dashboard: `python manage.py createsuperuser`

### Create an app in the project

Run command:
```bash
cd music_controller

django-admin startapp api
# OR
python manage.py startapp api
```

Then go into `02_django_react/music_controller/music_controller/settings.py` and add the name of
the app to the list.

### Adding a view

We can create a view in `02_django_react/music_controller/api/views.py`
```python
from django.http import HttpResponse
def main(request):
    return HttpResponse("<h1>hello</h1>")
```

Then create a new file `02_django_react/music_controller/api/urls.py` to hold URL paths.
```python
from django.contrib import admin
from django.urls import path
from .views import main
urlpatterns = [
    path('hello', main)
]
```

And we can include the URLs from our app by 'including' them in the project (root-level) URLs:
```python
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]
```

Then run the server (do migrations first):
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Note: the django server live-refreshes by default