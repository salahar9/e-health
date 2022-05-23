from django.urls import include, path
app_name="pharmacist"
from . import views
urlpatterns=[


	 path("dashboard/", views.dashboard, name="dashboard"),
	 path("register/", views.register, name="register"),
	 path("sales/", views.sales, name="sales"),
	 path("clients/", views.clients, name="clients"),
	 path("create_visite/", views.create_visite, name="create_visite"),
	 path("get_all/<int:pk>",views.get_all,name="get_all"),
	 path("ordo/<int:pk>",views.visite_ordo,name="ordo"),
	 path("ordomut/",views.mutuelle,name="mut")
]