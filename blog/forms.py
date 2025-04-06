from django import forms
from django.contrib.auth.models import User

class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=User.objects.all())