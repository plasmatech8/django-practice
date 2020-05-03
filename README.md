# django-practice
Following tutorial from https://www.youtube.com/watch?v=F5mRW0jo-U4

(mark, mark)

1. Basics (Apps)
2. Models
3. Routing
4. Templating
5. Forms

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

There are a lot more tags (`{% x %}`) and filters (`{{ x|y }}`).

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

## Django Model Forms

We will go into the `products` app and create `forms.py`.
```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]

```
Then we will create a view that renders this form in `views.py`.
```python
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "product2/product_create.html", context)
```
And create the temaplate:
```python
{% extends 'base.html' %}

{% block content %}
<form method='POST'> {% csrf_token %}
    {{ form.as_p }}
    <input type='submit' value='save' />
</form>
{% endblock %}
```
The `form.as_p` attribute will automatically render a Product creation form so we can create products from within a template. The `csrf_token` is needed for CSRF verification. Make sure that all required attributes of your product model is included in the form (`Meta`)

And lastly, add the new page to `urls.py`.

## Raw HTML Forms

We can also do raw custom HTML forms.

But if we click 'save', we will get forbidden, CSRF verification failed.

Also, if we use `method=GET` it only add a query string to and change the URL if we set action. i.e. Google Search:
```html
{% extends 'base.html' %}
{% block content %}
<form action='htttp://google.com/search' method='GET'>
    <input type='text' name='q' placeholder='Your search' />
    <input type='submit' value='save' />
</form>
{% endblock %}
```

To avoid the CSRF token verification issue on our website, we must include the `{% csrf_token %}` tag. Now the data can go to the webserver (but will return 403 error).

You can see your POST and GET data by using `request.POST` and `request.GET`.
```python
def product_create_view(request):
    print(request.GET)
    print(request.POST)  # QueryDict
    if request.method == "POST":
        new_title = request.POST.get('title')
        Products.objects.create(title=new_title, ...)
    context = {}
    return render(request, "product2/product_create.html", context)
```

This is a bad method of saving data because we still need to add validation and cleaning.

## Pure Django Forms

A Django form can also be created manually using the Django forms. i.e.
```python
from django import forms

class RawProductForm(forms.Form):
    title       = forms.CharField()
    description = forms.CharField()
    price       = forms.DecimalField()
```
We can then use the form the same way as Django model forms.
```python
def product_create_view(request):
    form = RawProductForm() # For GET
    if request.method == "POST":
        form = RawProductForm(request.POST) # For POST
        if form.is_valid():
            print(form.cleaned_data)  # Now the data is good
            Products.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, "product2/product_create.html", context)
```
A user can potentially disrupt the client-side form, so we can add validation as shown above.

It is also important to add the CSRF token.

> Django Model Forms are the best because they are directly attached to models with the webserver and database configured automatically.

## Form Widgets

We can change a lot about our model fields. i.e.
```python
class RawProductForm(forms.Form):
    title       = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder'='your title'
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'new-class-name',
                'rows': 2,
                'cols': 12,
                'id': 'new-id'
            }
        )
    )
    price       = forms.DecimalField(initial=99.99)
```
Now our custom/pure-Django form is almost identical to our Model Form.

> Another neat feature to note is that we can actually override the widgets of **Model Forms** by setting attributes on our class like how we did for pure-django/custom Forms: `title = forms.CharField()`.

## Form Validation Methods

We can use Django to validate our inputs.

We can use the `clean_<field-name>()` function to clean inputs.

```python
def clean_title(self, *args, **kwargs):
    title = self.cleaned_data.get('title')
    if 'fuck' in title.lower():
        raise forms.ValidationError("This is not a valid title")
    else:
        return title
```

Now expletive language does not pass validation for product names.

We can do all sorts of validation such as email checking, expletive removal, etc.
