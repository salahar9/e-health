from django.urls import path,url

from . import consumers

websocket_urlpatterns = [
    path(r'notif/<int:pk>/', consumers.VisiteConsumer.as_asgi()),

    url(r'^notif/pharma//(?P<room_name>[^/]+)/', consumers.VisitePharmaConsumer.as_asgi()),
]