from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from user_management.forms import UserRegistrationForm
from user_management.models import UserProfile


class UserRegistrationView(FormView):
    """
        # Access: Anonymous
    """

    template_name = 'user_management/user/create.html'
    form_class = UserRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        form = UserRegistrationForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            return render(request, self.template_name, context)

        user = form.save(commit=False)    # just get the form, but don't save to database yet
        password = form.cleaned_data['password']

        try:
            validate_password(password, user)
        except ValidationError as e:
            form.add_error('password', e)  # to be displayed with the field's errors
            return render(request, self.template_name, context)

        user.set_password(user.password)  # to hash the password
        user.save()  # save the new user with information to the database
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('/')


