from django.db import models
from django.contrib.auth.models import User


class Images(models.Model):
    original_images = models.ImageField(null=True)
    data_created = models.DateTimeField(auto_now_add=True)
    thumbnail_200 = models.ImageField(null=True, blank=True)
    thumbnail_400 = models.ImageField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    objects = models.Manager()

    def __str__(self):
        return self.original_images
