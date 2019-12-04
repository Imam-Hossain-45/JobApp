from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from settings.models import CompanyJobOffer


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
