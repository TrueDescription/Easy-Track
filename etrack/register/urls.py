from django.urls import path

from main import views as v


urlpatterns = [
#    path('<int:id>', v.index, name='index'),
    path('home/', v.home, name='home'),
]