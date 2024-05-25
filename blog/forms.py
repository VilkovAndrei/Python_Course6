from django import forms
from blog.models import Post
from main.forms import StyleFormMixin


class PostForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Post
        fields = 'title', 'description', 'preview', 'is_published'
