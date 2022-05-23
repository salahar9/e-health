from django.urls import path,re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'notif/(?P<room_name>\w+)/$', consumers.VisiteConsumer.as_asgi()),
    re_path(r'notif/pharma/(?P<room_name>\w+)/$', consumers.VisitePharmaConsumer.as_asgi()),

]