from django.shortcuts import render
"""
def basic_save(request, obj):
  obj.save()
  return None

def make_forms(request, *forms, **attrs):
  ret_forms = []
  if request.method == "POST":
    for index in range(len(forms)):
      temp = forms[index](request.POST, request.FILES, **attrs.get(f"args{index}",dict()))
      ret_forms.append(temp)
      if temp.is_valid():
        temp_ret = attrs.get(f"save{index}",basic_save)(request, temp)
        if temp_ret is not None:
          return temp_ret
  else:
    ret_forms = [forms[index](**attrs.get(f"args{index}",dict())) for index in range(len(forms))]
  return ret_forms

def make_form(request, form_t, form_save= basic_save, **args):
  if request.method == "POST":
    form = form_t(request.POST, request.FILES, **args)
    if form.is_valid():
      form_save(request, form)
  else:
    form = form_t(**args)
  return form
"""

class RenderForm():
  def __init__(self, request, form_t, view="single_form.html", *args,form_args=None, form_kwargs=None, view_kwargs=None,**kwargs):
    self.form_t = form_t
    self.request = request
    self.view = view
    self.form_args = list(form_args) if form_args is not None else []
    self.form_kwargs = form_kwargs if form_kwargs is not None else dict()
    self.view_kwargs = view_kwargs if view_kwargs is not None else dict()
    self.args = args
    self.kwargs = kwargs
    self.render = self._make_form()

  def _make_form(self):
    if self.request.method == "POST":
      self.form = self.form_t(*(self.form_args + [self.request.POST, self.request.FILES]), **self.form_kwargs)
      if self.form.is_valid():
        return self.save()
    else:
      self.form = self.form_t(*self.form_args, **self.form_kwargs)
    return self.default_render()
  
  def save(self):
    self.form.save()
    return self.default_render()
  
  def default_render(self):
    return render(self.request, self.view, {'form': self.form} | self.view_kwargs)
