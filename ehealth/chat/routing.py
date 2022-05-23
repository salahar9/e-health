
from chat import consumers
from django.urls import path,re_path

websocket_urlpatterns = [

re_path(r'notif/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),


]