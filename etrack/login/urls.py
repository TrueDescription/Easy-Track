from django.urls import path

from main import views as v
from register import views as v2


urlpatterns = [
    path('<int:id>', v.index, name='index'),
    path('home/', v.home, name='home'),
    path('login/register/', v2.register, name='register'),
]