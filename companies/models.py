from django.db import models as ms
from django.urls import reverse

class Company(ms.Model):
    name = ms.CharField(max_length=100, db_index=True)
    slug = ms.SlugField(unique=True)
    description = ms.TextField(blank=True)
    website = ms.URLField(blank=True)
    created_at = ms.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company-detail', kwargs={'slug': self.slug})
