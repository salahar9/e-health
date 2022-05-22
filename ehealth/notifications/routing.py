from django.urls import path
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    path(r'notif/<int:pk>/', consumers.VisiteConsumer.as_asgi()),
    url(r'notif/pharma/<int:pk>/', consumers.VisitePharmaConsumer.as_asgi()),
]