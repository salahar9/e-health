from django.urls import include, path
from . import views
app_name='chat'
urlpatterns=[
	path("",views.chats,name="chats"),

	path("<int:pk>/",views.chat,name="chat"),
	path("fetch/<int:pk>",views.fetch,name="fetch"),
	path("send_message/",views.sendmessage,name="sendmessage"),
	

]