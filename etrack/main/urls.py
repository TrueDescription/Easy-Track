from django.urls import path, include

from . import views
from register import views as v
from login import views as logv


urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('', views.home, name='home'),
    path('register/', v.register, name='register'),
    path('login/', logv.login, name='login'),
    path('login/register/', v.register, name='register'),
    path('', include("django.contrib.auth.urls")),
]