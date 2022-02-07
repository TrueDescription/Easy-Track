from django.db import models
from django.contrib.auth.models import User


# Create your models here.


"""
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # this will make sure that all to do lists are under some user
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text


class UserModel(models.Model):
    user_id = models.CharField(max_length=100)
    portfolio_mv = models.IntegerField()
    cash = models.IntegerField()
    total_deposits = models.IntegerField()
    dividends = models.IntegerField()
    history = models.JSONField()
    mv_history = models.JSONField()
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.user_id
"""