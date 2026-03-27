from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from .forms.forms import PostForm
from .forms.render import RenderForm
from .models import Post_Image

class RenderUserCreationForm(RenderForm):
  def __init__(self, request, *args, **kwargs):
    super().__init__(request, UserCreationForm, *args, **kwargs)

  def save(self):
    user = self.form.save()
    login(self.request, user)
    return redirect("update_profile")

class RenderAuthenticationForm(RenderForm):
  def __init__(self, request, *args, **kwargs):
    super().__init__(request, AuthenticationForm, form_args=[request], *args, **kwargs)

  def save(self):
    user = authenticate(self.request, **self.form.cleaned_data)
    if user is not None:
        login(self.request, user)
    return redirect("update_profile")


class RenderPostForm(RenderForm):
  def __init__(self, request, *args, **kwargs):
    super().__init__(request, PostForm, *args, **kwargs)

  def save(self):
    post = self.form.save(commit=False)
    post.user = self.request.user
    post.save()
    images = self.form.cleaned_data['images']
    for image in images:
      Post_Image.objects.create(post=post,image=image)
    return redirect('view_post',post_id=post.id)