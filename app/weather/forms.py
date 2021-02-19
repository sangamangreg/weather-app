from django import forms
from django.utils.translation import ugettext_lazy as _


class CityForm(forms.Form):
    city = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('Enter city')
        }))