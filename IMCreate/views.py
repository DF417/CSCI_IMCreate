from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms.forms import ProfileForm
from .forms.render import RenderForm
from .models import Post
from .render import RenderUserCreationForm, RenderPostForm, RenderAuthenticationForm


def front_page(request):
  return render(request, "index.html", {"posts": Post.objects.all})

def sign_up(request):
  if request.user.is_authenticated:
    return redirect("update_profile")
  return RenderUserCreationForm(request).render
  
def login_user(request):
  if request.user.is_authenticated:
    return redirect("update_profile")
  return RenderAuthenticationForm(request).render

def update_profile(request):
  if not request.user.is_authenticated:
    return login_user(request)
  print(request.user.profile.profile_pic)
  return RenderForm(request, ProfileForm, view='account.html', form_kwargs={"instance": request.user.profile}).render

def make_post(request):
  return RenderPostForm(request,view='make_post.html').render

def view_post(request, post_id):
  post = Post.objects.get(id=post_id)
  return render(request, 'components/post.html',{'post': post})
