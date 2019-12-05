from django import forms
from settings.models import JOB_TYPE_CHOICES as JOB_TYPE_CHOICES


class JobSearchByLocationForm(forms.Form):
    SEARCH_OPTION = (
        ('city', 'City'),
        ('state', 'State'),
        ('country', 'Country'),
    )
    search_by = forms.ChoiceField(choices=SEARCH_OPTION, label='Search By: ', initial='state', widget=forms.Select())


class JobSearchByPreferenceForm(forms.Form):
    preference = forms.ChoiceField(choices=JOB_TYPE_CHOICES, label='Search By: ', initial='', widget=forms.Select())
