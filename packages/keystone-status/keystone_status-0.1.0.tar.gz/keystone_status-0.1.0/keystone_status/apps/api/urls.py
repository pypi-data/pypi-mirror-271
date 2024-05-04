from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'api'

router = DefaultRouter()
router.register('service', ServiceViewSet, basename='service'),
router.register('status', StatusViewSet, basename='status'),
router.register('summary', SummaryViewSet, basename='summary')
urlpatterns = [
    path('', include(router.urls)),
    path('version/', lambda *args: HttpResponse(settings.VERSION), name='version'),
]
