from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.models import User, UserProfile, UserJobPreference
from user_management.forms import UserProfileUpdateForm, UserJobPreferenceForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class UserProfileDetailView(LoginRequiredMixin, TemplateView):
    """
    show the users profile detail
    """

    template_name = 'user_management/user/detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            context['job_preferences'] = UserJobPreference.objects.filter(user=self.request.user)
        return context


class UserProfileUpdateView(LoginRequiredMixin, FormView):
    """
    Update User Profile
    """
    template_name = 'user_management/user/update.html'
    form_class = UserProfileUpdateForm

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


class UserJobPreferenceUpdateView(LoginRequiredMixin, FormView):
    """
    Update User Job Preference
    """
    template_name = 'user_management/user/job_preference.html'
    form_class = UserJobPreferenceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = UserJobPreference.objects.filter(user=self.request.user)
        print(context['selected'])
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserJobPreferenceForm(request.POST)
        context['form'] = form

        if not form.is_valid():
            context['selected'] = UserJobPreference.objects.filter(user=self.request.user)
            return render(request, self.template_name, context)

        for i, component in enumerate(request.POST.getlist('job_type')):
            UserJobPreference.objects.update_or_create(
                user=self.request.user,
                job_preference=component
            )

        selected_list = request.POST.getlist('job_type')
        user_preferences = UserJobPreference.objects.filter(user=self.request.user)
        if user_preferences.exists():
            for member in user_preferences:
                selected = False
                for sel in selected_list:
                    if sel == member.job_preference:
                        selected = True
                if not selected:
                    member.delete()

        return redirect(reverse_lazy('user_management:user_detail', kwargs={'pk': kwargs.get('pk', '')}))


