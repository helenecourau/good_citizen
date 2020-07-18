from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'),
         name="home"),
    url('accueil',  TemplateView.as_view(template_name='home.html'),
        name="home"),
    ]