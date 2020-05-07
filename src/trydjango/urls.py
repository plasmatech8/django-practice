"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pages.views import (home_view, contact_view, about_view, social_view,
                         example_view)
from products.views import (product_detail_view, product_create_view,
                            product_dynamic_lookup_view, product_delete_view,
                            product_list_view)

urlpatterns = [
    path('', home_view),
    path('contact/', contact_view),
    path('about/', about_view),
    path('social/', social_view),
    path('example/', example_view),
    path('admin/', admin.site.urls),
    path('product/', product_detail_view),
    path('product/create/', product_create_view),
    path('product/<int:p_id>/', product_dynamic_lookup_view),
    path('product/<int:p_id>/delete/', product_delete_view),
    path('product/list/', product_list_view),
]
