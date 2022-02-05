from django.db import models
import sys
import datetime

sys.path.insert(0, 'C:/Users/faisa/PycharmProjects/Easy-Track')
from user import User


# Create your models here.


class ToDoList(models.Model):
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
    user_id = models.CharField(max_length=200)
    currency = models.CharField(max_length=3)
    #user_object = models.AutoField()
    user_object = User(str(user_id), datetime.datetime.now(), str(currency))
    #user_object


    def __str__(self):
        return self.user_id
