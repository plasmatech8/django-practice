# django-practice

## Setup

Open terminal/Anaconda prompt:
```
python -m venv env
```
Activate your environment
```
Windows: `.\env\Scripts\activate`
Mac/Linux: `source env/bin/activate`
```
Install django
```
pip install django==2.0.7
```

## Create Project

Create project
```
mkdir src
cd src
django-admin startproject trydjango .
```
You will see a `trydjango` folder and `manage.py`.

## Run the Server

Start server
```
python manage.py runserver
```
Open localhost:8000 and you will be greeted with django default page.
