from django.db import models 
from django.urls import reverse

class Company(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company-detail', kwargs={'slug': self.slug})
