
from core import consumers
from django.urls import path

websocket_urlpatterns = [
	path(r'/notif/convo/<int:pk>/', consumers.ChatConsumer.as_asgi()),

]