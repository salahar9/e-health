
from chat import consumers
from django.urls import path

websocket_urlpatterns = [

	path(r'pharma/<int:pk>/', consumers.ChatConsumer.as_asgi()),

]