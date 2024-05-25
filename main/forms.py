from django import forms
from main.models import Client, MessageMailing, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_blocked' and field_name != 'is_published':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'


class ClientAddForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('email', 'name', 'comment')


class MessageAddForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MessageMailing
        fields = ('subject', 'body')


class MallingAddForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Получаем текущего пользователя из kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request and self.request.user:
            self.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)

    class Meta:
        model = Mailing
        fields = ('start_time', 'frequency_mailing', 'status_mailing', 'clients', 'message')
