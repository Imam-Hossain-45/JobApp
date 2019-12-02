from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Main index view.

    Url: /
    """

    template_name = 'index.html'
