from django.urls import path

from jobboard import views
from django.contrib import admin
from django.urls import include, path

app_name = 'jobboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('', views.IndexView, name='index'),

    path('company/<int:pk>/', views.CompanyView.as_view(), name='company'),

    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),

    #path('search/', views.SearchView.as_view(), name='search'),

]