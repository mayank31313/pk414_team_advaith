from .views import *
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/crop/', CropApi.as_view(), name='crop'),
    path('api/price/', PriceApi.as_view(), name='price'),
    path('api/production/', ProductionApi.as_view(), name='price'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/',userDetails.as_view(),name='getuser'),
    path('api/failures/',FailureApi.as_view(),name='failure'),
    path('api/farm-start/',FarmModuleStart.as_view(), name = "Farm Planner"),
    path('api/distributer/',DistributerApi.as_view(),name = "distributer")
]