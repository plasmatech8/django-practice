from django.urls import path
# from .views import article_list_view, article_create_view, article_detail_view
from .views import (
    ArticleListView
)

app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list')

    # path('', article_list_view, name='article-list'),
    # path('create/', article_create_view, name='article-create'),
    # path('<int:a_id>/', article_detail_view, name='article-detail')
]
