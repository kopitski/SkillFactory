from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = {
            'title',
            'text',
            'post_category',
        }

    field_order = ['title', 'text', 'post_category',]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")
        if text == title:
            raise ValidationError({
                "Текст новости не должен быть идентичен названию"
            })

        return cleaned_data


class UserForm(forms.ModelForm):
   class Meta:
       model = User
       fields = [
           'username',
           'first_name',
           'last_name',
       ]