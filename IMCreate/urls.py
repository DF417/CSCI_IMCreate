from django.urls import path

from .views import front_page, follow_user, block_user, get_post, like_post, get_user, create_account

urlpatterns = [
  path("", front_page,name="front_page"),
  path("follow/<int:user_id>", follow_user, name="follow_user"),
  path("block/<int:user_id>", block_user, name="block_user"),
  path("post/<str:post_slug>",get_post, name="get_post"),
  path("like/<int:post_id>", like_post, name="like_post"),
  path("user/<int:user_id>", get_user, name="get_user"),
]