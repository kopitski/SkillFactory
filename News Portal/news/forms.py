from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    category_type = 'NW'

    class Meta:
        model = Post
        fields = {
            'author',
            'title',
            'text',
            'post_category',
        }

    field_order = ['author','title', 'text', 'post_category',]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")
        if text == title:
            raise ValidationError({
                "Текст новости не должен быть идентичен названию"
            })

        return cleaned_data