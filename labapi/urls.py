from rest_framework.routers import DefaultRouter
from django.urls import path, include
from labapi import views


app_name = 'labapi'

router = DefaultRouter()

router.register(r'order', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
