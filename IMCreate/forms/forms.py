from django import forms
from ..models import Post, Comment, Profile
from django.contrib.auth.models import User
from .fields import MultipleFileField

class UserCreateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'password']

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['display_name', 'about_me', 'profile_pic']
    widgets = {'profile_pic': forms.FileInput()}

class PostForm(forms.ModelForm):
  images = MultipleFileField()
  class Meta:
    model = Post
    fields = ['title', 'description', 'tags']

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']