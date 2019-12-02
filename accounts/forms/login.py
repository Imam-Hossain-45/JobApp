from django import forms


class LogInForm(forms.Form):
    """Login Form."""

    email = forms.EmailField(label='Email', error_messages={'required': "Enter email address"}, widget=forms.EmailInput(
        attrs={'placeholder': 'Email Address'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Password'}),
                               error_messages={'required': "Enter password"})

