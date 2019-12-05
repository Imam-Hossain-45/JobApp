from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.models import User


class UserListView(LoginRequiredMixin, ListView):
    """
    show all the users
    """

    template_name = 'user_management/user/list.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = User.objects.all()
        return context
