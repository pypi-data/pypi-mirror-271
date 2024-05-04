from django.urls import path, re_path
from django.views.generic import TemplateView

app_name = 'gui'

urlpatterns = [
    path('', TemplateView.as_view(template_name='summary.html'), name='summary')
]
