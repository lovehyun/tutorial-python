from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title
