from django import forms
from .models import User, Post, Comment
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
  display_name = forms.CharField()
  about_me = forms.CharField(widget=forms.Textarea)
  class Meta:
    model = User
    fields = ['profile_pic', 'username', 'password1', 'password2', 'display_name', 'about_me']
    widgets = {'password': forms.PasswordInput()}
class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'media', 'description', 'tags']

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']