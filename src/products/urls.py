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
    path('list/', product_list_view, name='product-list')
]
