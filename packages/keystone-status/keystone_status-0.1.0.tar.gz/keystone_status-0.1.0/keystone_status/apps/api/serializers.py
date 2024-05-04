from rest_framework import serializers

from .models import *

__all__ = ('ServiceSerializer', 'StatusSerializer', 'SummarySerializer')


class ServiceSerializer(serializers.ModelSerializer):
    """Data serializer for the `Service` model"""

    class Meta:
        model = Service
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    """Data serializer for the `Status` model"""

    class Meta:
        model = Status
        fields = '__all__'


class SummarySerializer(serializers.Serializer):
    """Data serializer for the `Service` model that includes a historical status summary"""

    def to_representation(self, instance: Service) -> dict:
        """Return a JSON serializable representation of a `Service` instance"""

        status_query = Status.objects.filter(service=instance).order_by('-time')

        service_json = ServiceSerializer(instance).data
        service_json['latest'] = StatusSerializer(status_query.first()).data
        service_json['history'] = StatusSerializer(status_query.all()[:5], many=True).data
        return service_json
