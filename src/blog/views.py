from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.


def article_list_view(request):
    queryset = Article.objects.all()  # list of objects
    context = {
        'obj_list': queryset
    }
    return render(request, "article_list.html", context)


def article_create_view(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('blog:article-list')
    context = {'form': form}
    return render(request, "article_create.html", context)


def article_detail_view(request, a_id):
    obj = get_object_or_404(Article, id=a_id)
    context = {
        'obj': obj
    }
    return render(request, "article_detail.html", context)
