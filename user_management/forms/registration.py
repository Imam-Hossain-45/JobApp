from django import forms
from user_management.models import User


class UserRegistrationForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm Password'}),
        error_messages={'required': "The password confirmation field is required."})

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.fields['password'].widget = forms.PasswordInput()
            self.fields['password_confirmation'].widget = forms.PasswordInput()
            self.add_error('password_confirmation', 'Password and Password confirmation do not match')
