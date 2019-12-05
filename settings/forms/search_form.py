from django import forms


class JobSearchByLocationForm(forms.Form):
    SEARCH_OPTION = (
        ('city', 'City'),
        ('state', 'State'),
        ('country', 'Country'),
    )
    search_by = forms.ChoiceField(choices=SEARCH_OPTION, label='Search By: ', initial='state', widget=forms.Select())
