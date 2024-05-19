from django import forms
from main.models import Client, MessageMailing, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientAddForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('email', 'name', 'comment')


class MessageAddForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MessageMailing
        fields = ('subject', 'body')


class MallingAddForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('start_time', 'frequency_mailing', 'status_mailing', 'clients', 'message')
