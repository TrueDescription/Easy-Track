from django.contrib import admin
from .models import Portfolio, Position, Transaction, WatchItem

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Position)
admin.site.register(Transaction)
admin.site.register(WatchItem)
