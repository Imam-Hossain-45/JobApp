from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('sign-up/', views.UserRegistrationView.as_view(), name='sign_up'),
]
