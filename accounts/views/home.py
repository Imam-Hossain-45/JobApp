from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Main index view.

    Url: /
    """

    template_name = 'index.html'
