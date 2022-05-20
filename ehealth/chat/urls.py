from django.urls import include, path
from . import views
app_name='chat'
urlpatterns=[

	path("chat/<int:pk>/",views.chat,name="chat"),
	

]