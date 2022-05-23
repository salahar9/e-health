from django.urls import path,re_path

from . import consumers

websocket_urlpatterns = [
    path(r'notif/<int:pk>/', consumers.VisiteConsumer.as_asgi()),
   # re_path(r'notif/pharma/(?P<room_name>\w+)/$', consumers.VisitePharmaConsumer.as_asgi()),

]