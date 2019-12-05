from django import forms
from settings.models import JOB_TYPE_CHOICES


class UserJobPreferenceForm(forms.Form):
    job_type = forms.MultipleChoiceField(
        choices=JOB_TYPE_CHOICES,
        required=False
    )
