from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('redditsearch/', views.reddit_search, name='reddit_search')

]
