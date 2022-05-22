from django.urls import include, path
app_name="pharmacist"
from . import views
urlpatterns=[


	 path("dashboard/", views.dashboard, name="dashboard"),
	 path("register/", views.register, name="register"),
	 path("sales/", views.sales, name="sales"),
	 path("clients/", views.clients, name="clients"),
	 path("create_visite/", views.clients, name="create_visite"),
]