from rest_framework import viewsets

from .models import *
from .serializers import *

__all__ = ('ServiceViewSet', 'StatusViewSet', 'SummaryViewSet')


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for listing services"""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for listing service status checks"""

    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class SummaryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for summarising a service's status"""

    queryset = Service.objects.all()
    serializer_class = SummarySerializer
