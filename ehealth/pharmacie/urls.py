from django.urls import include, path
from . import views

app_name = "pharmacist"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("sales/", views.sales, name="sales"),
]
