from django.urls import path, re_path
from .views import index

urlpatterns = [
    #path('', index),
    #path('<path:resource>', index),
    re_path(r'^.*$', index)
]
