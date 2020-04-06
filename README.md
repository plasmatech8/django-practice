# django-practice
Following tutorial from https://www.youtube.com/watch?v=F5mRW0jo-U4

(mark, mark)

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
pip install django
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

## Create an app

Apps are really good at storing data and mapping to your database. Apps are more like components than like 'mobile apps'.

Initialise an app.
```
python manage.py startapp products

e.g.
python manage.py startapp blog
python manage.py startapp profiles
python manage.py startapp cart
```

We can now add the app to `INSTALLED_APPS` in our `settings.py`.

Update the data model in [src/products/models.py](src/products/models.py) in our new app.
```python
class Product(models.Model):
    title       = models.TextField()
    description = models.TextField()
    price       = models.TextField()
```

Use commands `python manage.py makemigrations` and `python manage.py migrate` to update the models in the database. These are important to use every time we update our models.

Now we can register the model to the app by adding `admin.site.register(Product)` to [src/products/admin.py](src/products/admin.py) 

Now we can run the server and register new products in the admin page. (with `python manage.py runserver` and go to http://127.0.0.1:8000/admin)

## Create Product Objects in the Python Shell

We used the admin webpage before, now we will use Python shell.

```bash
python manage.py shell
```
```python
from products.models import Product
Product.objects.all()
```
`>>> <QuerySet [<Product: Product object (1)>]>`

```python
Product.objects.create(title='New product 2', 
                       description='another one',
                       price='19423',
                       summary='sweet')
Product.objects.all()
```
`>>> <QuerySet [<Product: Product object (1)>, <Product: Product object (2)>]>`

Now you can start the server (`python manage.py runserver`) and see your newly created objects.
