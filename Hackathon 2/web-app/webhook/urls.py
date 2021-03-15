from django.urls import path
from .views import (
    FacebookWebhookView
)


urlpatterns = [
    path('', FacebookWebhookView.as_view(), name='root'),
]