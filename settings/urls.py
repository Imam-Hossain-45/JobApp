from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.AllJobsView.as_view(), name='all_jobs_list'),
]
