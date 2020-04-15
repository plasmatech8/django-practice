from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})


def contact_view(request, *args, **kwargs):
    return render(request, 'contact.html', {})


def about_view(request, *args, **kwargs):
    my_context = {
        'my_text': 'This is about us',
        'my_number': 123,
        'my_list': ['a', 'b', 'c', 'd']
    }
    return render(request, 'about.html', my_context)


def social_view(request, *args, **kwargs):
    return render(request, 'social.html', {})


def example_view(request, *args, **kwargs):
    print('Request:  ', request)
    print('User:     ', request.user)
    print(args, kwargs)
    return HttpResponse('<h1>Example View</h1>') # String of HTML