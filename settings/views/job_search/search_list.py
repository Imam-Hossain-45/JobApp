from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from settings.models import CompanyJobOffer
from settings.forms import JobSearchByLocationForm, JobSearchByPreferenceForm
from django.shortcuts import render
from user_management.models import UserJobPreference


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


class PreferredJobList(LoginRequiredMixin, TemplateView):
    """
        show all the jobs for the user by preference
        """

    template_name = 'settings/job_search/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            context['search_criteria'] = 'Preferred Jobs'
            user_job_preferences = UserJobPreference.objects.filter(user=self.request.user)
            jobs = []
            context['form'] = JobSearchByPreferenceForm()
            for job_preference_obj in user_job_preferences:
                company_job_offers = CompanyJobOffer.objects.filter(job_type=job_preference_obj.job_preference)
                if company_job_offers.exists():
                    for company_job_offer in company_job_offers:
                        jobs.append(company_job_offer)

            context['jobs'] = jobs
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = JobSearchByPreferenceForm(request.POST)
        context['form'] = form
        context['search_criteria'] = 'Preferred Jobs'
        if not form.is_valid():
            return render(request, self.template_name, context)

        preference = form.cleaned_data['preference']
        print(preference, type(preference))

        if preference == 'none':
            user_job_preferences = UserJobPreference.objects.filter(user=self.request.user)
            jobs = []
            for job_preference_obj in user_job_preferences:
                company_job_offers = CompanyJobOffer.objects.filter(job_type=job_preference_obj.job_preference)
                if company_job_offers.exists():
                    for company_job_offer in company_job_offers:
                        jobs.append(company_job_offer)
            context['jobs'] = jobs

        else:
            context['jobs'] = CompanyJobOffer.objects.filter(job_type=preference)

        return render(request, self.template_name, context)
