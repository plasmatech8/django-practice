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

# New (Better) Model Fields

We will update `src/products/models.py` because the title is too long, price is passed as a string, etc.

We can delete all the files in the migrations folder, the pycache directory, and the sqlite database. This means starting everything over.

See the Django field type reference: https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-types

```python
class Product(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price       = models.DecimalField(decimal_places=2, max_digits=1000)
    summary     = models.TextField(default="This is cool!")    
```

Now make migrations and recreate super user:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Use `python manage.py migrate --run-syncdb` if you run into operational error, no such table issues.

Now when you attempt to add new products in the admin age, the fields will have fixed input length, and input validation is performed.

# Change a Model

I am going to make a change to the model without deleting the database or migrations.

Make migrations and migrate syncs the database to the models in our code.

If we add a non-nullable field to our model (e.g. a boolean field called 'featured'), then when we make migrations, we will be asked to either make it nullable or use a default value for the new fields in old records.

We need to do: `null=True` or `default=<value>` in code. Or we can provide a one-off default when prompted.

Note: `blank=True` means that the field can be blank (different from null).

# Change Default Homepage to Custom Homepage

Let's create an app called `pages`. (`python manage.py startapp products` and add to `INSTALLED_APPS`)

Go to [views.py](src/pages/views.py).

We can use Python classes or functions to return our webpages.

Let's create `home_view` function.

Afterwards we will need to update [urls.py](src/trydjango/urls.py). Notice that we already have the path `admin/` set to the admin page. We can add the  `pages.views.home_view` function to the `''` path.

Now we have a new homepage.

# URLs Routing and Requests

In our view function, a `<WSGIRequest: GET>` object is passed in. 

We can see requst information. 

`request.user` is the user. If you are logged in as admin it will be the admin username. If you open an incognito window, it will be AnnoymousUser.

# Django Templates

Instead of writing strings in our view functions, we want to have templates.

For this we can use the Django rendering engine (`django.shortcuts.render`).

Our view functions can return `render(request, 'home.html', {})` to return a rendered view, with a context dictionary.

We can create the folder `src/templates` and create `home.html`. 

Also, make sure you add the `templates` directory to `settings.py`. Add the directory by doing: `'DIRS': [os.path.join(BASE_DIR, 'templates')]` in the `TEMPLATES` list.

Now our templates are being used in the webpage!
