from django.urls import include, path
from . import views
app_name='chat'
urlpatterns=[

	path("chat/",views.chat,name="chat"),
	

]