
from chat import consumers
from django.urls import path

websocket_urlpatterns = [
	path(r'notif/chat/<int:pk>/', consumers.ChatConsumer.as_asgi()),

]