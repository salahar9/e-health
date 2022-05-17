from . import views
from django.urls import path
app_name="landing"

urlpatterns = [
        path("", views.index, name="index"),
        path("login/", views.login_user, name="login"),
        path("register/", views.register_user, name="register"),
        path("redirect/<int:loginp>",views.re_redirect,name="redirect"),
        path("json_check/",views.login_json,name="json_check"),
        path("card/",views.patient_from_card,name="card"),
        path("profileregister/",views.profile_register,name="profile_register"),
        path("changing_pic/",views.changing_pic,name="change_pic"),
        path("logout/",views.logout_view,name="logout")


]
