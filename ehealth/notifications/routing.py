from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'notif/<int:pk>/', consumers.VisiteConsumer.as_asgi()),

    path(r'^notif/pharma//(?P<room_name>[^/]+)/', consumers.VisitePharmaConsumer.as_asgi()),
]