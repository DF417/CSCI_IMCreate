from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from taggit.managers import TaggableManager
from PIL import Image

#have to download + include 'taggit' in the INSTALLED_APPS
#pillow -> for image size validations
"""
TODO: in settings.py
Caps the file upload automatically

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
"""

profiles = "profiles/"
posts = "posts/"

def validate_pfp(image):
  img = Image.open(image)
  if img.size != (400,400):
    raise ValidationError("Image must be 400x400.")

class UserManager(BaseUserManager):
  """
  TODO: profile picture here?
  """
  def create_user(self, username, password=None, **extra_fields):
    if not username:
      raise ValueError("Username required.")
    user = self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

#TODO: edit AUTH_USER_MODEL to be -> "app.User" in settings.py
class User(AbstractBaseUser, PermissionsMixin):
  """
  
  TODO: add default profile_pic, image compression.

  The data for a user.

  Attributes:
  username: User's log-in username.
  display_name: User's display name.
  about_me: User's about me.
  profile_pic: User's profile pic.
  date: Date User joined.
  """
  username = models.CharField(max_length = 50, unique = True)
  display_name = models.CharField(max_length = 50)
  about_me = models.TextField(max_length = 1000)
  profile_pic = models.ImageField(upload_to = profiles, validators = [validate_pfp])
  date = models.DateField(auto_now_add = True)
  object = UserManager()
  USERNAME_FIELD = 'username'

class Post(models.Model):
  """

  TODO: All media, just images, file compression.

  The data for a post.

  Attributes:
  user: User that posted post.
  upload_date: Post upload date.
  edit_date: Last edit date.
  title: User provided title.
  media: User provided media.
  description: user provided description.
  tags: User provided tags.
  slug: Unique slug for url.
  """
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  upload_date = models.DateTimeField(auto_now_add = True)
  edit_date = models.DateTimeField(auto_now = True)
  title = models.CharField(max_length = 255)
  media = models.FileField(upload_to = posts)
  description = models.TextField(max_length = 1000)
  tags = TaggableManager()
  slug = models.SlugField(unique = True)

class Comment(models.Model):
  """

  The data for comments.

  Attributes:
  user: The User that posted the comment.
  last_edit_date: Last edit date of the comment.
  comment: The text of the comment.
  post: The post the comment is linked to.
  parent: If part of a comment chain on a post, the parent comment, else None.
  """
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  last_edit_date = models.DateTimeField(auto_now = True)
  comment = models.TextField(max_length = 1000)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  parent = models.ForeignKey("self", null=True,blank=True,on_delete=models.CASCADE,related_name="replies")

class Like(models.Model):
  """

  The data for likes.

  Attributes:
  user: User that gave the like.
  post: Post that the user liked.
  """
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  class Meta:
    constraints = [models.UniqueConstraint(fields=['user', "post"], name = 'unique_like')]

class Follower(models.Model):
    """

    The data for following a specific user.

    Attributes:
    following: Account that is being followed.
    follower: User that is following.
    notifications: If the follower gets notifs when following posts.
    """
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='following')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='follower')
    notifications = models.BooleanField(default = True)
    class Meta:
      # unique_together = ("follower", "following")
      constraints = [models.UniqueConstraint(fields=['follower', "following"], name = 'unique_follow')]

class Blocked(models.Model):
    """
    Blocked Accounts.

    Attributes:
    blocked_user: The account that is blocked.
    blocker: The account that did the blocking.
    """
    blocker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='blocker')
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked')
    class Meta:
      # unique_together = ("blocker", "blocked_user") getting deprecated
      constraints = [models.UniqueConstraint(fields=['blocker', "blocked_user"], name = 'unique_block')]