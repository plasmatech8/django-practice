from django.shortcuts import render, get_object_or_404, redirect
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
    obj = get_object_or_404(Product, id=p_id)
    context = {
        "obj": obj
    }
    return render(request, "product2/detail.html", context)


def product_delete_view(request, p_id):
    obj = get_object_or_404(Product, id=p_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('../..')

    context = {
        "obj": obj
    }
    return render(request, "product2/product_delete.html", context)


def product_list_view(request):
    queryset = Product.objects.all()  # list of objects
    context = {
        'obj_list': queryset
    }
    return render(request, "product2/product_list.html", context)
