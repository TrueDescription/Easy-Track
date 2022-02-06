from django.urls import path
from . import views
from etrack.register import views as v


urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('', views.home, name='home'),
    path('register/', v.register, name='register')
]