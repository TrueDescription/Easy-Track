from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as t


# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio', null=True)
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
    date = models.DateField(default=t.now)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    Position = models.ForeignKey(Position, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    ticker = models.CharField(max_length=5)
    shares = models.IntegerField()
    avg_cost = models.IntegerField()
    date = models.DateField(default=t.now)

    def __str__(self):
        return self.name


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class WatchItem(models.Model):
    name = models.CharField(max_length=100, default='')
    ticker = models.CharField(max_length=5)

    def __str__(self):
        return self.name
