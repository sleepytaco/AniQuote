from django.db import models


# Create your models here.
class Quote(models.Model):
    anime = models.CharField(max_length=150, default="N/A")
    character = models.CharField(max_length=150, default="N/A")
    quote = models.CharField(max_length=1500, default="N/A")

    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=1)
