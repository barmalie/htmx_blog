from django.db import models
from django.contrib.auth.models import User
from companies.models import Company
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)
    summary = models.TextField(max_length=500)
    content = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})

    def likes_count(self):
        return self.likes.count()
