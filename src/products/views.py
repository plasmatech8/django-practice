from django.shortcuts import render
from .models import Product
from .forms import ProductForm

# Create your views here.


def product_create_view(request):
    # obj = Product.objects.get(id=1)  # We can use instance=obj to update an existing record
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "product2/product_create.html", context)


def product_detail_view(request):
    obj = Product.objects.get(id=1)
    # context = {
    #     'title': obj.title,
    #     'description': obj.description,
    #     'price': obj.price
    # }
    context = {'obj': obj}
    return render(request, "product2/detail.html", context)


def product_dynamic_lookup_view(request, p_id):
    print(p_id)
    obj = Product.objects.get(id=p_id)
    context = {
        "obj": obj
    }
    return render(request, "product2/detail.html", context)
