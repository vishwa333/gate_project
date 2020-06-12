"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('add',views.add,name='add'),
    path('tests',views.tests,name='tests'),
    path('step2',views.step2,name='step2'),
    path('step3',views.step3,name='step3'),
    path('start_test',views.start_test,name='start_test'),
    path('get_question',views.get_question,name='get_question'),
    path('store_result',views.store_result,name='store_result'),
    path('view_result',views.view_result,name='view_result'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)