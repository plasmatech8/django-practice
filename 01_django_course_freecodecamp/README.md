# django-practice
Following tutorial from https://www.youtube.com/watch?v=F5mRW0jo-U4

(mark, mark)

1. Getting Started
    * Create Project
    * Run the Server
1. App Basics
    * Create an app
    * Create Product Objects in the Python Shell
    * Add New Fields for our Model
    * Change a Model
    * Change Default Homepage to Custom Homepage
    * URLs Routing and Requests
1. Django Templating Engine
    * Django Templates
    * Django Templating Engine Basics
    * Include Template Tag
    * Rendering Context in a Template (backend rendering)
    * For Loop in a Template
    * Using Conditions in a Template
    * Template Tags and Filters
    * Render Data from our Database
    * How Django Templates Load with Apps
1. Django Forms
    * Django Model Forms
    * Raw HTML Forms
    * Pure Django Forms
    * Form Widgets
    * Form Validation Methods
    * Initial Values for Forms (+ updating existing records)
1. Dynamic Routing & Database Object Handling
    * Dynamic URL Routing
    * Handle DoesNotExist
    * Delete and Confirm
    * View a List of Database Objects
    * Dynamic Linking of URLs (dynamic updating of URLs - names, models, and templates)
1. Routing/Namespacing
    * Django URLs Reverse (dynamic updating of URLs - names, models, and templates)
    * In App URLs and Namespacing (dynamic updating of URLs - names, models, and templates)
1. Break
1. Class Based Views
    * Class Based Views
    * ListView
    * DetailView
    * CreateView
    * UpdateView
    * DeleteView
    * Converting Function-based to Class-based views (Raw Views)
    * Generic vs Raw Class-Based Views

## 01. Getting Started

### Create Project

Create project
```
mkdir src
cd src
django-admin startproject trydjango .
```
You will see a `trydjango` folder and `manage.py`.

### Run the Server

Start server
```
python manage.py runserver
```
Open localhost:8000 and you will be greeted with django default page.

## 02. App Basics

### Create an app

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

### Create Product Objects in the Python Shell

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

### Add New Fields for our Model

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

### Change a Model

I am going to make a change to the model without deleting the database or migrations.

Make migrations and migrate syncs the database to the models in our code.

If we add a non-nullable field to our model (e.g. a boolean field called 'featured'), then when we make migrations, we will be asked to either make it nullable or use a default value for the new fields in old records.

We need to do: `null=True` or `default=<value>` in code. Or we can provide a one-off default when prompted.

Note: `blank=True` means that the field can be blank (different from null).

### Change Default Homepage to Custom Homepage

Let's create an app called `pages`. (`python manage.py startapp products` and add to `INSTALLED_APPS`)

Go to [views.py](src/pages/views.py).

We can use Python classes or functions to return our webpages.

Let's create `home_view` function.

Afterwards we will need to update [urls.py](src/trydjango/urls.py). Notice that we already have the path `admin/` set to the admin page. We can add the  `pages.views.home_view` function to the `''` path.

Now we have a new homepage.

### URLs Routing and Requests

In our view function, a `<WSGIRequest: GET>` object is passed in.

We can see requst information.

`request.user` is the user. If you are logged in as admin it will be the admin username. If you open an incognito window, it will be AnnoymousUser.

## 03. Django Templating Engine

### Django Templates

Instead of writing strings in our view functions, we want to have templates.

For this we can use the Django rendering engine (`django.shortcuts.render`).

Our view functions can return `render(request, 'home.html', {})` to return a rendered view, with a context dictionary.

We can create the folder `src/templates` and create `home.html`.

Also, make sure you add the `templates` directory to `settings.py`. Add the directory by doing: `'DIRS': [os.path.join(BASE_DIR, 'templates')]` in the `TEMPLATES` list.

Now our templates are being used in the webpage!

### Django Templating Engine Basics

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

### Include Template Tag

Now lets move our navbar into another HTML document named `navbar.html`.

We can add this to `base.html` by using `{% include 'navbar.html' %}`.

### Rendering Context in a Template (backend rendering)

We can render our HTML using the context dictionary.

We can update the context dictionary in `views.py` and add `{{ my_text }}` to obtain the value from the dictionary.

### For Loop in a Template

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

### Using Conditions in a Template

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

### Template Tags and Filters

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

### Render Data from our Database

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

### How Django Templates Load with Apps

If we want to bundle our products page/templates, we can create a `templates` directory inside the app directory. (i.e. if we are creating a 3rd party app for other people)

We will create the template `src/products/templates/product2/detail.html`, and change the template used within `src/products/views.py` to `product2/detail.html` (within app) instead of `product/detail.html` (in the templates directory).

Note: No configuration in `settings.py` is needed for the view to access the template from inside the same app. (as long as `'APP_DIRS': True`)

Note: Ensure that the paths to templates do not conflict to avoid confusion. Paths are checked in a specific order. We can override defaul django templates if we wanted to.

## 04. Django Forms

### Django Model Forms

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

### Raw HTML Forms

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

### Pure Django Forms

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

> Django **Model** Forms are the best because they are directly attached to models with the webserver and database configured automatically.

### Form Widgets

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

### Form Validation Methods

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

### Initial Values for Forms (+ updating existing records)

We can set initial values for forms from within our `view.py` by creating a dictionary and passing into the `RawProductForm`.

```python
initial_data = {'title'='My title'}
form = RawProductForm(request.POST or None, initial_data=initial_data)
context = {'form': form}
return render(request, 'products/products_create.html', context)
```
It the same regardless to whether we use a Model Form or a Django Form.

We can also update an existing record with auto-filled content. (initial data overrides)

```python
obj = Products.objects.get(id=1)
form = RawProductForm(request.POST or None, instance=obj)
if form.is_valid():
    form.save()
context = {'form': form}
return render(request, 'products/products_create.html', context)
```

## 05. Dynamic Routing & Database Object Handling

### Dynamic URL Routing

Now we will change the content based on the URL.

We want to be able to pass in an ID into the URL and get a different resonse. i.e. http://127.0.0.1:8000/product/1/

To do this we use the url path: `path('product/<int:p_id>', product_dynamic_lookup_view)`.

And not the variable is being passed into the view function:
```python
def product_dynamic_lookup_view(request, p_id):
    obj = Product.objects.get(id=p_id)
    context = {
        "obj": obj
    }
    return render(request, "product2/detail.html", context)
```
Now we are rendering a new product for each id.

### Handle DoesNotExist

If the product with the id does not exist, an error page will show up. We will import the `django.shortcuts.get_object_or_404` function and use that to handle this situation.

Now we get page not found error instead of product does not exist.

We can alternatively use a `try` block and raise a `django.http.Http404`.

### Delete and Confirm

We will create a product deletion form (the form itself acts as confirmation page).

We will create a page `product2/product_delete.html`, create a view `product_delete_view(request, p_id)`, and route a path to it `path('product/<int:p_id>/delete/', product_delete_view)`.

`obj.delete()` deletes a record, but we want to do this using a POST request, not using GET.

In our view, we will use:
```python
if request.method == 'POST':
        obj.delete()
        return redirect('../..')
```
To delete the object when the DELETE button is clicked, and redirect back to the base `products/` page.

### View a List of Database Objects

We will create the `product2/product_list.html` template which uses for-loop template tags, then create the `product_list_view(request)` view which stores all products in the database as a list in the context, then add the view to the `product/list/` URL.


### Dynamic Linking of URLs (dynamic updating of URLs - names, models, and templates)

We want to add links to each products in our list of products.

We can use a `<a href='/products/{{ instance.id }}'>` tag to link to the product, but if the structure of the URL changes, it will break.

What we can do instead, is add a `get_absolute_url` function on our product model (convention):
```python
def get_absolute_url(self):
    return f"/products/{self.id}/"
```

And use in our template:
```html
<a href='{{ instance.get_absolute_url }}'>{{ instance.title }} - ${{ instance.price }}</a>
```

But there is an more-standardised/better way...

## 06. Routing/Namespacing

### Django URLs Reverse (dynamic updating of URLs - names, models, and templates)

We can give URLs names:
```python

urlpatterns = [
    path('', home_view),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('social/', social_view, name='social'),
    path('example/', example_view, name='example'),
    path('admin/', admin.site.urls, name='admin'),
    path('product/', product_detail_view, name='product'),
    path('product/create/', product_create_view, name='product-create'),
    path('product/<int:p_id>/', product_dynamic_lookup_view, name='product-detail'),
    path('product/<int:p_id>/delete/', product_delete_view, name='product-delete'),
    path('product/list/', product_list_view, name='product-list'),
]
```
And link make our via name:
```python
def get_absolute_url(self):
    return reverse("product-detail", kwargs={"p_id": self.id})
```
Now we can use the URL name instead of the resource path for URLs.

If we change the resource path, then the links in our code will continue working since we are using the names.

> I see a very small benefit to this compared to just using the resource path, but it is the standard.

Now, we need to make the links for our nav bar dynamic (and other templates if they have links). This will make it so that we can change our resource paths, while URLs in the **code** and **templates** can be dynamically updated.

Making template URLs dynamic can be done using the `url` template tag (same as `reverse` in the server).
```html
<nav>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="{% url 'about' %}">About</a></li>
        <li><a href="{% url 'product' %}">Product</a></li>
        <li><a href="{% url 'contact' %}">Contact</a></li>
        <li><a href="{% url 'social' %}">Social</a></li>
        <li><a href="{% url 'example' %}">Example</a></li>
    </ul>
</nav>
```

### In App URLs and Namespacing (dynamic updating of URLs - names, models, and templates)

We have a lot of views to import, and what if we use more than one name for a single path? Ans: bad.

We can move the product Paths from the `urls.py` in `trydjango` into the `products` app. Then (as described in comments) we can import the urls **ON TOP** of a base path in the `urls.py` in `trydjango`.

`urls.py` in `products`:
```python
from django.urls import path
from products.views import (product_detail_view, product_create_view,
                            product_dynamic_lookup_view, product_delete_view,
                            product_list_view)

app_name = 'products'
urlpatterns = [
    path('', product_detail_view, name='product'),
    path('create/', product_create_view, name='product-create'),
    path('<int:p_id>/', product_dynamic_lookup_view, name='product-detail'),
    path('<int:p_id>/delete/', product_delete_view, name='product-delete'),
    path('list/', product_list_view, name='product-list'),
]
```

`urls.py` in `trydjango`:
```python
path('product/', include('products.urls')),
```

`app_name` (namespace) was added because these URLs are in a different file and it is possible to accidently make duplicate named pages.

We now MUST reverse the URL using `<app_name>:<url_name>`. e.g. `products:product-detail`.

If we did not add the namespace, it is still possible to access it via the URL name without the app namespace (`<app_name>:`).

We will need to add the `products:` namespace to the start of every reverse/url in the code and in the templates.

> Basically, we have the choice to do routing via URL paths or names (+ namespaces). Using paths is simpler, but names allow for paths to update dynamically in views (+models). Names + namespaces are the best practice.

## 07. Break

The next few will use previous knowledge gained

1. Create a new App named Blog
2. Add 'Blog' to your Django project
3. Create a Model named Article
4. Run Migrations
5. Create a ModelForm for Article
6. Create `article_list.html` & `article_detail.html` template
7. Add Article Model to the Admin
8. Save a new Article object in the admin

## 08. Class Based Views

### Class Based Views

We can create class-based views (instead of function-based views) in `views.py` using standard django views.

e.g.
```python
from django.views.generic import (
    CreateView,
    DetailView
    ListView,
    UpdateView,
    DeleteView,
)
class ArticleListView(ListView):
    template_name = 'articles/article_list.html'
    queryset = Article.objects.all()
```

We can make class-based views inherit standard view functionality so we do not need to write much code.

Pros:
* Code reusability
* Code extendability (inherit functionality from standard views and mixins)
* Code structuring (seperate functions for post and get)

Cons:
* Harder to read
* Harder to understand functionality
* Inheritance

See:
* https://medium.com/@ksarthak4ever/django-class-based-views-vs-function-based-view-e74b47b2e41b
* http://ccbv.co.uk/

It is up to you to decide whether to use class or function based views.

Class based views that do not inherit any standard-views/functionality can also be used. This will provide nice code structure and allow you to inherit later if you wish.

### ListView

ListView will supply a list from a queryset.
```python
class ArticleListView(ListView):
    template_name = 'article_list.html'  # DEFAULT: <blog>/<modelname>_list.html
    queryset = Article.objects.all()  # REQUIRED
```
The objects passed into the context as: `object_list`.

### DetailView

`pk` stands for Primary Key. It is the same as the record ID. You need to use `pk` in the URL path to point towards the record.
```python
class ArticleDetailView(DetailView):
    queryset = Article.objects.all()
    template_name = 'article_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")  # Get object from URL with different dynamic URL variable name
        return get_object_or_404(Article, id=id_)
```
The object is passed into the context as: `object`.

> To allow our model to expect a different URL integer other than `pk`, we can override built-in methods like get_object if we wanted to.

> We can use `queryset = Article.objects.filter(id__gt=2)` to restrict viewable objects to >2 if we wanted to.

### CreateView

We can create a create view by using the same attributes, plus our form model class to specify the form fields.
```python
class ArticleCreateView(CreateView):
    queryset = Article.objects.all()
    template_name = 'article_create.html'
    form_class = ArticleForm

    def get_object(self):
        id_ = self.kwargs.get("pk")  # Get object from URL
        return get_object_or_404(Article, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
```
The form is passed into the context as: `form`.

> Upon submission (POST), it will redirect the user to the detail-view using the model `get_absolute_url`. This also applies to update-view. (override using `success_url` attribute or `get_success_url` function).

> There is also a `form_valid`/`form_invalid` function which can be used.


### UpdateView

> As we create more views, notice how inheritance can be really good by providing all classes the same get_object methods.

We can create an update-view which is almost identical to create-view.

```python
class ArticleUpdateView(UpdateView):
    queryset = Article.objects.all()
    template_name = 'article_update.html'
    form_class = ArticleForm

    def get_object(self):
        id_ = self.kwargs.get("pk")  # Get object from URL
        return get_object_or_404(Article, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
```
The form is passed into the context as: `form`.

### DeleteView

Very similar to detail-view. We will use the same template as we did for the product-delete-view.

```python
class ArticleDeleteView(DeleteView):
    # queryset = Article.objects.all()
    template_name = 'article_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")  # Get object from URL
        return get_object_or_404(Article, id=id_)

    def get_success_url(self):
        return reverse('blog:article-list')
```

The form is passed into the context as: `object`.

> We need to make sure we define a get_success_url function.

### Converting Function-based to Class-based views (Raw Views)

Class-based views are nice.
```python
from django.shortcuts import render
from django.views import View

# CLASS BASED VIEW


class ExampleView(View):
    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        pass


# FUNCTION BASED VIEW


def example_view(request, *args, **kwargs):
    return render(request, 'about.html', {})

```
If we wanted to override the template_name, we could do `ExampleView.as_view(template_name='contact.html'` in `urls.py`.

We can use the same template for two different pages if we wanted to.

#### Raw Detail C-B-View

We can set an `id` as None by default if we wanted to, to make it optional.
```python
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Course


class CourseView(View):
    template_name = "course_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        if id is not None:
            context['object'] = get_object_or_404(Course, id)
        return render(request, self.template_name, context)
```

#### Raw List C-B-View

List views are simple. The inheritance property is good because we can make child classes with filtered querysets...?
```python
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Course


class CourseListView(View):
    template_name = "course_list.html"
    queryset = Course.objects.all()

    def get_querset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_querset()}
        return render(request, self.template_name, context)
```

#### Raw Create C-B-View

```python
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Course
from .forms import CourseModelForm


class CourseCreateView(View):
    template_name = "course_create.html"

    def get(self, request, *args, **kwargs):
        form = CourseModelForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CourseModelForm(request.POST)
        if form.is_valid():
            form.save()
            form = CourseModelForm()
        context = {'form': form}
        return render(request, self.template_name, context)
```
Note: to refresh the form page, you can simply pass a new form object into the context.

Model Form:
```python
from django import forms
from .models import Course


class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
        ]

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if 'fuck' in title:
            raise forms.ValidationError('Explicit language. Invalid title')
        return title
```

#### Raw Update C-B-View

`get_object` is made so it works in both our get and post methods.
```python
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Course
from .forms import CourseModelForm


class CourseUpdateView(View):
    template_name = "course_update.html"

    def get_object(self):
        id = self.kwargs.get('id')
        if id is not None:
            return get_object_or_404(Course, id=id)
        return None

    def get(self, request, *args, **kwargs):
        """View the details and update form for an object"""
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = CourseModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Save the data for an object"""
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = CourseModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)
```

> Note: C-B-view `self.kwargs.get('id')` == F-B-view `dynamic_lookup_view(request, id)`

#### Raw Delete C-B-View

```python
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Course
from .forms import CourseModelForm


class CourseDeleteView(View):
    template_name = "course_delete.html"

    def get_object(self):
        id = self.kwargs.get('id')
        if id is not None:
            return get_object_or_404(Course, id=id)
        return None

    def get(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('/courses/')
        return render(request, self.template_name, context)
```

### Generic vs Raw Class-Based Views

You can see all the logic and variables in raw class-based views, but it can get a bit redundant.

Generic C-B views are simpler and cleaner, only requiring few parameters and overloading.

### Custom Mixins for Class Bsed Views

Mixins allow us to extend C-B views with new code.

This mixin can be used to create the get_object function (defauling to the Course model).

```python
class CourseObjectMixin(object):
    model = Course

    def get_object(self):
        id = self.kwargs.get('id')
        if id is not None:
            return get_object_or_404(self.model, id=id)
        return None
```

This will help reduce redundancy in my code. i.e. `CourseDeleteView(CourseObjectMixin, View)`. Mixin must come first.

We can also use this to replace the `if id is None` and `get_object_or_404` logic, because  the function in the mixin handles this  for us.
