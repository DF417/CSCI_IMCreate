from django.forms.fields import FileField
from .widgets import MultipleFileInput

class MultipleFileField(FileField):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault("widget",MultipleFileInput(attrs={'accept': 'image/png, image/jpeg'}))
    super().__init__(*args,**kwargs)
  def clean(self,data,initial=None):
    single_file_clean = super().clean
    if isinstance(data, (list, tuple)):
      result = [single_file_clean(d, initial) for d in data]
    else:
      result = [single_file_clean(data, initial)]
    return result
