from django.contrib import admin
from django.urls import path

from .views import hello, ListRoomView, CreateRoomView

urlpatterns = [
    path('hello', hello),
    path('rooms', ListRoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
]
