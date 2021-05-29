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
  - [02. Django Models + REST Framework](#02-django-models--rest-framework)
    - [Create Database model](#create-database-model)
    - [Use REST framework to create a model record (POST)](#use-rest-framework-to-create-a-model-record-post)
    - [Use REST framework to list model records](#use-rest-framework-to-list-model-records)

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

Then go into `music_controller/settings.py` and add the name of
the app to the list.

### Adding a view

We can create a view in `api/views.py`
```python
from django.http import HttpResponse
def main(request):
    return HttpResponse("<h1>hello</h1>")
```

Then create a new file `api/urls.py` to hold URL paths.
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

## 02. Django Models + REST Framework

### Create Database model

Go into `api/models.py`:
```python
from django.db import models
import string
import random

def generate_unique_code():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            return code

class Room(models.Model):
    code = models.CharField(max_length=8, default="", unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    # ... other attributes & methods if desired
```
* Added the Room model for music room
* Added a function to create unique code

Django prefers fat models, and thin views.
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Use REST framework to create a model record (POST)

The Django Rest Framework just makes it slightly easier to serialize/deserialize data for
front-end use (especially for a model).

Add to `rest_framework` to INSTALLED_APPS in `music_controller/settings.py`.

Create `api/serializers.py`:
```python
from rest_framework import serializers
from .models import Room
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause',
                  'votes_to_skip', 'created_at')
```

Then we can update our `api/views.py`:
```python
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room
# ...
class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
```

Then we can add the endpoint to our `api/urls.py`:
```python
from django.contrib import admin
from django.urls import path
from .views import hello, RoomView
urlpatterns = [
    path('hello', hello),
    path('rooms/create', RoomView.as_view()),
]
```

Now we can go to `http://127.0.0.1:8000/api/rooms/create` and we will be greeted to a REST
Framework API page! **We can now CREATE NEW rooms using POST requests!**

> Django Rest Framework vs Django Model Forms: DRF is better in a sense, because it allows us to
> easily make a REST framework with less boilerplate. Also, Django model forms require using the
> back-end templating to inject a token. Django model forms are useful for form rendering though.

### Use REST framework to list model records


Changing our endpoing from CREATE to LIST is as simple as changing the inheritance in the view:
```python
class RoomView(generics.ListAPIView):
```