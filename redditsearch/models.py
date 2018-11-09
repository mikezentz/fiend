from django.db import models

# Create your models here.


class Search(models.Model):
    searchname = models.CharField(max_length=128)
    subreddits = models.CharField(max_length=1024)
    searchterms = models.CharField(max_length=2048)

    def __str__(self):
        return self.searchname
