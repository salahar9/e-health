from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'notif/<str:pk>/', consumers.VisiteConsumer.as_asgi()),
    path(r'notif/pharma/<int:pk>/', consumers.VisitePharmaConsumer.as_asgi()),
]