from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import User, Post, Comment, Like, Follower, Blocked
from .forms import UserForm, PostForm, CommentForm

def front_page(request):
  return create_account(request)

def create_account(request):
  success = False
  account = None
  if request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      success = True
      return redirect('front_page')
  else:
    form = UserForm()
  return render(request, "account.html", {"form": form, "success": success},)

def follow_user(request, user_id):
  print(f"[DBG] follow_user {user_id} <<<")
  current_user = request.User
  if request.method == "POST" and current_user.is_authenticated:
    Follower.objects.create(following=User.objects.get(id=user_id), follower=current_user)

  return redirect(request.path)

def block_user(request, user_id):
  print(f"[DBG] block_user {user_id} <<<")
  current_user = request.User
  if request.method == "POST" and current_user.is_authenticated:
    Blocked.objects.create(blocked_user=User.objects.get(id=user_id), blocker=current_user)

  return redirect(request.path)

def get_post(request, post_slug):
  post = get_object_or_404(Post, slug=post_slug)
  return render(request, "components/post.html",post = post)

def like_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)
  user = request.User
  if user.is_authenticated and post:
    Like.objects.create(user=user, post=post)
  return redirect(request.path)

def get_user(request, user_id):
  user = User.objects.get(id=user_id)
  return render(request, "user_page.html", user=user)