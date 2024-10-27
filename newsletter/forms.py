from django import forms
from .models import Newsletter, Client


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['message', 'scheduled_at', 'periodicity', 'clients']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'middle_name','email',)


