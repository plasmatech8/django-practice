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

## Add New Fields for our Model 

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

## Change a Model

I am going to make a change to the model without deleting the database or migrations.

Make migrations and migrate syncs the database to the models in our code.

If we add a non-nullable field to our model (e.g. a boolean field called 'featured'), then when we make migrations, we will be asked to either make it nullable or use a default value for the new fields in old records.

We need to do: `null=True` or `default=<value>` in code. Or we can provide a one-off default when prompted.

Note: `blank=True` means that the field can be blank (different from null).

## Change Default Homepage to Custom Homepage

Let's create an app called `pages`. (`python manage.py startapp products` and add to `INSTALLED_APPS`)

Go to [views.py](src/pages/views.py).

We can use Python classes or functions to return our webpages.

Let's create `home_view` function.

Afterwards we will need to update [urls.py](src/trydjango/urls.py). Notice that we already have the path `admin/` set to the admin page. We can add the  `pages.views.home_view` function to the `''` path.

Now we have a new homepage.

## URLs Routing and Requests

In our view function, a `<WSGIRequest: GET>` object is passed in. 

We can see requst information. 

`request.user` is the user. If you are logged in as admin it will be the admin username. If you open an incognito window, it will be AnnoymousUser.

## Django Templates

Instead of writing strings in our view functions, we want to have templates.

For this we can use the Django rendering engine (`django.shortcuts.render`).

Our view functions can return `render(request, 'home.html', {})` to return a rendered view, with a context dictionary.

We can create the folder `src/templates` and create `home.html`. 

Also, make sure you add the `templates` directory to `settings.py`. Add the directory by doing: `'DIRS': [os.path.join(BASE_DIR, 'templates')]` in the `TEMPLATES` list.

Now our templates are being used in the webpage!

## Django Templating Engine Basics

There is a lot of things in common between each of the pages we created and we do not want to duplicate work in multiple files and make things messy. (Headers, CSS, Javascript, nav bars, etc)

So we should use **template inheritance** -> A root page for our other pages to inherit from.

The name: `base.html` is the convention.

We can write:
```html
{% block content %}
    replace me
{% endblock %}
```
In the places in our base.html that we want replace with child content.

Now we must extend our child content by surrounding it with block replace tags and adding an inheritance tag. 

i.e.
```html
{% extends 'base.html' %}

{% block content %}
<h1>Hello World</h1>
{{ request.user }} <br>
{{ request.user.is_authenticated }} <br>
<p>This is a template.</p>
{% endblock %}
```

Note that 'content' is the name of the blocks.

## Include Template Tag

Now lets move our navbar into another HTML document named `navbar.html`.

We can add this to `base.html` by using `{% include 'navbar.html' %}`.

## Rendering Context in a Template (backend rendering)

We can render our HTML using the context dictionary.

We can update the context dictionary in `views.py` and add `{{ my_text }}` to obtain the value from the dictionary.

## For Loop in a Template

We want to print the list called 'my_list' in the context dictionary into a `<ul>`.

We can loop through our list using `{% for item in list %}` and `{% endfor %}` tags.

i.e.
```html
<ul>
    {% for my_item in my_list %} 
    <li>{{ forloop.counter }} - {{ my_item }}</li>
    {% endfor %}
</ul>
```

`{{ forloop.counter }}` can also be used to obtain the iteration number.

## Using Conditions in a Template

Usually we want most if-else statements to occur in the view and not the template, but there are cases where it is suitable to do this in the template.

We can create an if-else statement like:
```html
{% if my_item == 5 %}  
    <li>Item {{ forloop.counter }} plus 22 = {{ my_item|add:22 }}</li>
{% else %}
    <li>Item {{ forloop.counter }} = {{ my_item }}</li>
{% endif %}
```

See the documentation for build-in template tags: https://docs.djangoproject.com/en/3.0/ref/templates/builtins/

## Template Tags and Filters

So far we have used several build-in template tags:
* extends
* block
* for
* if

There are a lot more (`{% x %}`). i.e.
* comment
* cycle
* debug
* filter
* firstof
* for ... empty
* ifchanged
* include
* load
* lorem
* now
* regroup
* resetcycle
* spaceless
* url
* verbatim
* widthratio
* with

And filters (`{{ x|y }}`). i.e.
* add `{{ value|add:second }}`
* addslashes
* capfirst
* centre
* cut
* date
* default
* default_if_none
* dictsort
* divisibleby
* escape
* escapejs
* filesizeformat
* first
* floatformat
* force_escape
* get_digit
* iriencode
* join
* json_scrip
* last
* length
* lenth_is
* linebreaks
* linebreaksbr
* linenumbers
* ljust
* lower
* make_list
* phone2numeric
* pluralize
* pprint
* random
* rjust
* safe
* safeseq
* slice
* slugify
* stringformat
* striptags
* time
* timesince
* timeuntil
* title
* truncatechars
* truncatechars_html
* truncatewords
* truncatewords_html
* unordered_list
* upper
* urlencode
* urlize
* urlizetrunc
* wordcount
* wordwrap
* yesno
* etc

You can even use multiple filters at the same time.

e.g. 
* `{{ title|title }}`
* `{{ body|lower|capfirst }}`
* `{{ my_html|safe }}` (renders HTML)
* `{{ address|slugify }}`

## Render Data from our Database 

Open `python manage.py shell`
```python
from products.models import Product

obj = Product.objects.get(id=1)

obj.title
```

We want everything related to products to be under the `products` app, so we will add a new view to `src/products/views.py` called `product_detail_view`.

```python
def product_detail_view(request):
    obj = Product.objects.get(id=1)
    # context = {'title': obj.title, 'description': obj.description, 'price': obj.price}
    context = {'obj': obj}
    return render(request, "product/detail.html", context)
```

Django has an inhuilt feature: all records have an auto-incrementing ID field.

We will create a new template under `src/templates/product/detail.html`.
```html
{% extends 'base.html' %}

{% block content %}
<h1>Product: {{ obj.title }}</h1>
<p>{% if obj.description != None and obj.description != '' %}{{ obj.description }}
    {% else %}No description{% endif %}</p>
<p>Price: ${{ obj.price }}</p>
{% endblock %}
```
## How Django Templates Load with Apps

If we want to bundle our products page/templates, we can create a `templates` directory inside the app directory. (i.e. if we are creating a 3rd party app for other people)

We will create the template `src/products/templates/product2/detail.html`, and change the template used within `src/products/views.py` to `product2/detail.html` (within app) instead of `product/detail.html` (in the templates directory).

Note: No configuration in `settings.py` is needed for the view to access the template from inside the same app. (as long as `'APP_DIRS': True`)

Note: Ensure that the paths to templates do not conflict to avoid confusion. Paths are checked in a specific order. We can override defaul django templates if we wanted to.

https://youtu.be/F5mRW0jo-U4?t=7610