from django.db import models

__all__ = ('Service', 'Status')


class Service(models.Model):
    """Metadata for individual backend services"""

    name = models.CharField(max_length=100, unique=True)


class Status(models.Model):
    """Status check results for backend services"""

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.IntegerField()
    message = models.TextField(null=True)
    time = models.DateTimeField(auto_now_add=True)
