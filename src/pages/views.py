from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_view(*args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>") # String of HTML


def contact_view(request, *args, **kwargs):
    print('Request:  ', request)
    print('User:     ', request.user)
    print(args, kwargs)
    return HttpResponse('<h1>Contact View</h1>')