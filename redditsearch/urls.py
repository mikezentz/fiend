from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('test/', views.test, name='test'),
    path('redditsearch/', views.reddit_search, name='reddit_search'),
    path('delete/<str:id>', views.search_delete, name='search_delete'),

]
