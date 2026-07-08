from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = [
            'default_phone_number',
            'default_street_address1',
            'default_street_address2',
            'default_town_or_city',
            'default_postcode',
            'default_country',
        ]
        labels = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Address Line 1',
            'default_street_address2': 'Address Line 2',
            'default_town_or_city': 'Town / City',
            'default_postcode': 'Postcode',
            'default_country': 'Country',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
