import uuid
def img_path(directory):
  return f"{directory}{uuid.uuid4().hex}.jpeg"

def pfp_path(instance, filename):
  return img_path(f"{instance.user.id}/pfp/")

def post_image_path(instance, filename):
  return img_path(f"{instance.post.user.id}/posts/")