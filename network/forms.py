from django import forms
from django.db import models
from django.forms import fields
from django.utils.translation import gettext_lazy as _
from .models import *

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["postTitle", "postBody"]
        labels = {
            "postTitle": _("Post Title"),
            "postBody": _("Post Body")
        }
        widgets = {
            'postTitle' : forms.TextInput(attrs={'class' : 'form-control'}),
            'postBody' : forms.Textarea(attrs={'class' : 'form-control', "rows" : "5", "style" : "resize: none;", "maxlength": "500"})            
        }