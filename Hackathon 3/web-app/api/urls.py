from django.urls import path
from .views import FacebookWebhookView, CustomFetchView

urlpatterns = [
    path('fetch/<str:category>', CustomFetchView, name='custom-fetch-view'),
    path('webhook/', FacebookWebhookView.as_view(), name='webhook-view'),
]