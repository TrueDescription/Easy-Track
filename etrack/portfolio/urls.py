from django.urls import path, include

from . import views
from register import views as v
from login import views as logv
from portfolio import views as pv


urlpatterns = [
#    path('<int:id>', views.index, name='index'),
    path('portfolio/<str:name>', views.home, name='dashboard'),
]