from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'notif/<int:pk>/', consumers.VisiteConsumer.as_asgi()),
    path(r'pharmavisite/<int:pk>/', consumers.VisitePharmaConsumer.as_asgi()),
]