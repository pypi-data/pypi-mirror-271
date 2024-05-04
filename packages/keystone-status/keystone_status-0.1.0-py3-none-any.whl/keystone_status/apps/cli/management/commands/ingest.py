import argparse

import requests
from django.core.management.base import BaseCommand

from apps.api.models import Service
from apps.api.serializers import StatusSerializer


class Command(BaseCommand):
    """Ingest status data from a given URL"""

    help = __doc__

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Define arguments for the command line interface"""

        parser.add_argument('url', type=str, help='URL to ingest data from')

    def handle(self, *args, **kwargs) -> None:
        """Execute application logic against parsed arge"""

        try:
            response = requests.get(kwargs['url'])
            data = response.json()

            for service_name, status in data.items():
                service, _ = Service.objects.get_or_create(name=service_name)

                status['service'] = service.id
                status['status_code'] = service.id
                serializer = StatusSerializer(data=status)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        except Exception as exception:
            self.stderr.write(str(exception))
            exit(1)
