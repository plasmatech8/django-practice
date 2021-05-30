# Django & React

See:
* [Django & React Tutorial ](https://www.youtube.com/watch?v=JD-age0BPVo) By Tech With Tim on YouTube
* Consider taking inspiration from [this template](https://github.com/scottwoodall/django-react-template/) (esp for csrf token)

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
  - [03. React integration (w/ Webpack)](#03-react-integration-w-webpack)
    - [Create new app for frontend](#create-new-app-for-frontend)
    - [Configuration files](#configuration-files)
    - [Initialize Template & React files](#initialize-template--react-files)
    - [Initialise Django View & URLs](#initialise-django-view--urls)
    - [Build and run](#build-and-run)
  - [04. React Router + Components](#04-react-router--components)
  - [05. POST Requests (create room)](#05-post-requests-create-room)
  - [06. Frontend POST Request (Create Room page)](#06-frontend-post-request-create-room-page)

Suggestions:
* Use a different module bundler other than webpack
* Use different frontend folder structure. i.e. `src`, `build` or `static/js`, `templates`
* Put css and assets into React src
* `manage.py` usually at root level of repo
* If we want, it is possible to have apps inside folders or sub-apps, and we can reference them using dot notation.

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

## 03. React integration (w/ Webpack)

### Create new app for frontend

Create app with command: `django-admin startapp frontend`

Update the `settings.py`: `'frontend',`

Create folders:
```
cd frontend \
mkdir \
  templates \
  templates/frontend \
  static \
  static/frontend \
  static/css \
  static/images \
  src \
  src/components
```

Create NPM project with command: `npm init -y`
```bash
npm i webpack webpack-cli --save-dev
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev

npm i @babel/plugin-proposal-class-properties
npm i react react-dom --save-dev
npm i react-router-dom

npm i @material-ui/core
npm i @material-ui/icons
```
* webpack for module bundling
* babel for browser compatability (ES6, etc)
* @babel/plugin-proposal-class-properties for async await (???)


### Configuration files

We will create/copy:
* `babel.config.json`
* `webpack.config.json`

Add to `package.json`:
* Create a 'dev' script: `"dev": "webpack --mode development --watch",`
* Create a 'build' script: `"build": "webpack --mode production",`

### Initialize Template & React files

Create root template file, `templates/frontend/index.html`:
```html
<!-- ... -->
  {% load static % }
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
  />
  <link rel="stylesheet" type="text/css" href="{% static "css/index.css" %}"/>
  <script src="{% static "frontend/main.js" %}" defer></script>
<!-- ... -->
  <div id="main">
    <div id="app"></div>
  </div>
```
* We will use load static to load files from the static directory, and load our JS and CSS.

Create React entry point file, `index.js`:
```js
import { render } from "react-dom";
import App from "./components/App";
const appDiv = document.querySelector('#app')
render(<App/>, appDiv);
```

Create React app component:
```jsx
import React, { Component } from "react";
function App() {
  return (
    <div>
      <h1>Hello World!</h1>
      <p>Wahoo!!!</p>
    </div>
  )
}
export default App
```

Django will use send the template to the client, which is controlled by the React application.

### Initialise Django View & URLs

Add the view to `frontend/views.py`:
```python
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')
```

Create `frontend/urls.py` and add the URL:
```python
from django.urls import path
from .views import index
urlpatterns = [
    path('', index),
]
```

Include the frontend URLs in `music_controller/urls.py`:
```python
# ...
    path('', include('frontend.urls')),
# ...
```

### Build and run

We can now do:
```bash
npm run build
python manage.py runserver
```

We can see our webpage!

We can also use `npm run dev` to update the frontend.

> Note: IDK why we need a `templates/frontend` folder. And it seems nicer change the folder name
> from `static/frontend` to `static/js`

> Note: I personally think the file structure is better as:
> * `src/*` <- contains all css/js and assets
> * `templates/index.html`
> * `build/<css|js|img>`
> And have the module bundler

## 04. React Router + Components

We will create pages:
* HomePage
* CreateRoomPage
* JoinRoomPage
* NotFoundPage

We will add React router:
```jsx
<Router>
  <Link to="/join">Link to JOIN room</Link>

  <Switch>
      <Route exact path='/' component={HomePage} />
      <Route exact path='/join' component={JoinRoomPage} />
      <Route exact path='/create' component={CreateRoomPage} />
      <Route component={NotFound}/>
  </Switch>
</Router>
```

We can change the change the URL to a `re_path` so that we can match all paths to the React App:
```python
urlpatterns = [
    re_path(r'^.*$', index)
]
```

## 05. POST Requests (create room)

We want an API endpoint to create a room:
* `guest_can_pause` and `votes_to_skip` are input parameters in the request
* `created_at` and `created_at` are generated on automatically using model defaults
* `host` must be obtained by using from the session key, managed by a custom APIView

In `api/serializers.py`, We will create a new serializer for create-room requests:
```python
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')
```

In `api/views.py`, we could use `CreateAPIView`, but we need to use a custom `APIView` to get the
session/host:
```python
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # If the user does not have a session, create a session
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # Get data from request & serializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            # Update the room if the host already owns a room, else Create new room
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()

            # Return a response of the record created
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        # Error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Then we update `api/urls.py` to show the additional page under `/api/create-room`.

We can see the returned record, and update it too (but only for fields shown in the serializer).

> **Possibly not best practice**.
> It is best RESTful practice to organise the resource paths differently:
> * GET /rooms
> * POST /rooms
> * PATCH /rooms/0
> * PUT /rooms/0
> * DELETE /rooms/0
>
> Use ViewSets or ModelViewSet to add multiple APIs to the same view (TODO)
>
> Although, I do not know if it is best practice for endpoints with customized inputs (like above)
> should be placed under `POST /rooms` or `POST /create-room`, since the JSON is different from
> the raw data.

## 06. Frontend POST Request (Create Room page)

We can create React code to submit a POST request to our endpoint.

```js
  const [guestCatPause, setGuestCanPause] = useState(true);
  const [votesToSkip, setVotesToSkip] = useState(1);
  const handleGuestCanPause = (e) => setGuestCanPause(e.target.value === 'true')
  const handleVotesToSkip = (e) => setVotesToSkip(parseInt(e.target.value))
  const handleSubmit = async (e) => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guest_can_pause: guestCatPause, votes_to_skip: votesToSkip })
    }
    const response = await (await fetch('/api/create-room', requestOptions)).json()
    console.log(response)
  }
```

