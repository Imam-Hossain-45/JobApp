from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.AllJobsView.as_view(), name='all_jobs_list'),
    path('nearby/', views.NearbyJobList.as_view(), name='nearby_jobs_list'),
    path('preferences/', views.PreferredJobList.as_view(), name='preferred_jobs_list'),
]
