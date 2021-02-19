from django import forms


class CityForm(forms.Form):
    city = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter city'
        }))