from django.contrib import admin
from django.urls import path


from . import views

urlpatterns = [
    path('select_test',views.select_test,name='select_test')
    #path('signup', views.signup, name='signup'),
]