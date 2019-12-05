from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from settings.models import CompanyJobOffer
from settings.forms import JobSearchByLocationForm
from django.shortcuts import render


class AllJobsView(LoginRequiredMixin, ListView):
    """
    show all the jobs for the user
    """

    template_name = 'settings/job_search/list.html'
    model = CompanyJobOffer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_criteria'] = 'All Jobs'
        context['jobs'] = CompanyJobOffer.objects.all()
        return context


class NearbyJobList(LoginRequiredMixin, TemplateView):
    """
        show all the jobs for the user by location
        """

    template_name = 'settings/job_search/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            context['form'] = JobSearchByLocationForm()
            context['search_criteria'] = 'Nearby Jobs'
            if self.request.user.userprofile.state:
                context['jobs'] = \
                    CompanyJobOffer.objects.filter(
                        company__companyphysicaladdress__state__name=self.request.user.userprofile.state
                    )
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = JobSearchByLocationForm(request.POST)
        context['form'] = form
        context['search_criteria'] = 'Nearby Jobs'
        if not form.is_valid():
            return render(request, self.template_name, context)

        search_by = form.cleaned_data['search_by']

        if search_by == 'country':
            if self.request.user.userprofile.country:
                context['jobs'] = \
                    CompanyJobOffer.objects.filter(
                        company__companyphysicaladdress__country=self.request.user.userprofile.country
                    )

        elif search_by == 'state':
            if self.request.user.userprofile.country:
                context['jobs'] = \
                    CompanyJobOffer.objects.filter(
                        company__companyphysicaladdress__state__name=self.request.user.userprofile.state
                    )

        elif search_by == 'city':
            if self.request.user.userprofile.city:
                context['jobs'] = \
                    CompanyJobOffer.objects.filter(
                        company__companyphysicaladdress__city__name=self.request.user.userprofile.city
                    )

        return render(request, self.template_name, context)
