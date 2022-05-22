from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'notif/<int:pk>/', consumers.VisiteConsumer.as_asgi()),
    path(r'notif/pharma/<int:pk>/', consumers.VisitePharmaConsumer),
]