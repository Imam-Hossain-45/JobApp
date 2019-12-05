from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout as auth_logout
from accounts.forms import LogInForm


class LogInView(FormView):
    """
    Show a login form to log a user in.

    Url: /accounts/login/
    """
    form_class = LogInForm
    template_name = 'accounts/log_in.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(username=email, password=password)

        if user is None:
            messages.error(self.request, 'Sorry, we did not find any matching user with the provided credentials')

            return redirect(reverse_lazy('accounts:login'))

        if user.is_active:
            login(self.request, user)
            return redirect(reverse_lazy('settings:all_jobs_list'))

        messages.error(self.request, 'The user is inactive. Please contact with administrator')

        return redirect(reverse_lazy('accounts:login'))


class LogOutView(LoginRequiredMixin, RedirectView):
    """
    Log a user out.

    Url: /accounts/logout/
    """

    def get_redirect_url(self, *args, **kwargs):
        auth_logout(self.request)

        return reverse_lazy('accounts:login')
