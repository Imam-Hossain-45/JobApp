from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('sign-up/', views.UserRegistrationView.as_view(), name='sign_up'),
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('<pk>/', views.UserProfileDetailView.as_view(), name='user_detail'),
    path('<pk>/update/', views.UserProfileUpdateView.as_view(), name='user_update'),
]
