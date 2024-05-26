from django import forms
from django.core.exceptions import ValidationError

from blog.models import Post
from main.forms import StyleFormMixin


class PostForm(StyleFormMixin, forms.ModelForm):
    max_upload_limit = 4 * 1024 * 1024

    class Meta:
        model = Post
        fields = 'title', 'description', 'preview'

    def clean_preview(self):
        image = self.cleaned_data.get('preview', False)
        if image:
            if image.size > self.max_upload_limit:
                raise ValidationError("Файл с картинкой очень большой ( > 4mb )")
            return image
        else:
            raise ValidationError("Не могу прочитать загруженную картинку")
