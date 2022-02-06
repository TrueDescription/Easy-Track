from django.urls import path, include

from . import views
from register import views as v
from login import views as logv
from portfolio import views as pv


urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('', views.home, name='home'),
    path('register/', v.register, name='register'),
    path('login/', logv.login, name='login'),
    path('login/register/', v.register, name='register'),
    path('', include("django.contrib.auth.urls")),
    path('logout/', logv.logoutUser, name='logoutUser'),
    path('portfolio/', pv.portfolioView, name='portfolio'),
]