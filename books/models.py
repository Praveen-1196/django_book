from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    quote = models.TextField()
    image = models.URLField()   # Will store Cloudinary URL

    def __str__(self):
        return self.name
