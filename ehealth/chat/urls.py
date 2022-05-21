from django.urls import include, path
from . import views
app_name='chat'
urlpatterns=[
	path("/",views.chats,name="chat"),

	path("<int:pk>/",views.chat,name="chat"),
	

]