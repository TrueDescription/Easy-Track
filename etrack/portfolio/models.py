from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField()
    name = models.CharField(max_length=100, default='Portfolio')

    def __str__(self):
        return self.name


class Position(models.Model):
    Portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=100, default='')
    shares = models.IntegerField()
    avg_cost = models.IntegerField()

    def __str__(self):
        return self.name


