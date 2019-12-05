from django import forms
from user_management.models import UserProfile


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address_line1', 'address_line2', 'zip_code', 'city', 'state', 'country', 'date_of_birth')
