from operator import mod
from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as t
import yfinance as yf


# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio', null=True)
    balance = models.FloatField(default=0)
    name = models.CharField(max_length=100, default='Portfolio')
    total_deposits = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def drop(self):
        self.balance -= 100


class Position(models.Model):
    Portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='position', null=True)
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=100, default='')
    shares = models.FloatField(default=0)
    avg_cost = models.FloatField(default=0)
    date = models.DateField(default=t.now)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    Position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='transaction', null=True)
    name = models.CharField(max_length=100, default='')
    ticker = models.CharField(max_length=5)
    shares = models.FloatField(default=0)
    avg_cost = models.FloatField(default=0)
    date = models.DateField(default=t.now)

    def __str__(self):
        return self.name


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist', null=True)
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class WatchItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='WatchItem', null=True)
    ticker = models.CharField(max_length=5)
    curr_price = models.FloatField(default=0)
    name = models.CharField(max_length=100, null=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker

