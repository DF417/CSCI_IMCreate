from django.urls import path

from .views import front_page, update_profile, make_post, view_post

urlpatterns = [
  path("", front_page,name="front_page"),
  path("account",update_profile, name="update_profile"),
  path("make_post",make_post,name="make_post"),
  path("post/<int:post_id>/",view_post,name="view_post"),
]