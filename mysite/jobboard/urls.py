from . import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'jobs', views.JobViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
# app_name = 'jobboard'
# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     #path('', views.IndexView, name='index'),
#
#     path('company/<int:pk>/', views.CompanyView.as_view(), name='company'),
#
#     path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
#
#     #path('search/', views.SearchView.as_view(), name='search'),
#
# ]
