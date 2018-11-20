from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Search(models.Model):
    searchname = models.CharField(max_length=128)
    subreddits = models.CharField(max_length=1024)
    searchterms = models.CharField(max_length=2048)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='searches')

    def __str__(self):
        return self.searchname
