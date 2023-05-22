
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("edit_post/<int:id>", views.edit_post, name="edit_post"),
    path("following", views.following, name="following"),
    path("like/<int:id>", views.like, name="like"),
    path("delete/<int:id>", views.delete, name="delete")
]

