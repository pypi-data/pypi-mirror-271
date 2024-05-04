"""Top level URL configuration."""

from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='status')),
    path('status/', include('apps.gui.urls')),
    path('api/', include('apps.api.urls')),
]
