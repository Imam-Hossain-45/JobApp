from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.models import UserProfile
from user_management.forms import UserProfileUpdateForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class UserProfileDetailView(LoginRequiredMixin, TemplateView):
    """
    show the users profile detail
    """

    template_name = 'user_management/user/detail.html'


class UserProfileUpdateView(LoginRequiredMixin, FormView):
    """
    Update User Profile
    """
    template_name = 'user_management/user/update.html'
    form_class = UserProfileUpdateForm
    #
    # success_url = reverse_lazy('user_management:user_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = {
            'phone': self.request.user.userprofile.phone,
            'address_line1': self.request.user.userprofile.address_line1,
            'address_line2': self.request.user.userprofile.address_line2,
            'zip_code': self.request.user.userprofile.zip_code,
            'city': self.request.user.userprofile.city,
            'state': self.request.user.userprofile.state,
            'country': self.request.user.userprofile.country,
            'date_of_birth': self.request.user.userprofile.date_of_birth,
        }
        context['form'] = self.form_class(initial=initial)
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserProfileUpdateForm(request.POST)
        context['form'] = form

        if not form.is_valid():
            return render(request, self.template_name, context)

        user_profile = UserProfile.objects.get(user__id=kwargs.get('pk', ''))
        user_profile.phone = form.cleaned_data['phone']
        user_profile.address_line1 = form.cleaned_data['address_line1']
        user_profile.address_line2 = form.cleaned_data['address_line2']
        user_profile.zip_code = form.cleaned_data['zip_code']
        user_profile.country = form.cleaned_data['country']
        user_profile.state = form.cleaned_data['state']
        user_profile.city = form.cleaned_data['city']
        user_profile.date_of_birth = form.cleaned_data['date_of_birth']
        user_profile.save()

        return redirect(reverse_lazy('user_management:user_detail', kwargs={'pk': kwargs.get('pk', '')}))


