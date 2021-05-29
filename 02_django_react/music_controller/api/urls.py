from django.contrib import admin
from django.urls import path

from .views import hello, RoomView

urlpatterns = [
    path('hello', hello),
    path('rooms', RoomView.as_view()),
]
