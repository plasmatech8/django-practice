from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.


class Article(models.Model):
    text = models.TextField(blank=True, null=False)
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog:article-detail', kwargs={'pk': self.id})
