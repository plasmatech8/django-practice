from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

from .serializers import RoomSerializer
from .models import Room

# Django Views

def hello(request):
    return HttpResponse("<h1>hello</h1>")

# REST Framework Views

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer