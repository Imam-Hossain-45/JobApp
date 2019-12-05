from django.db import models
from helpers.models import Model
from settings.models import JOB_TYPE_CHOICES as JOB_TYPE_CHOICES


class UserJobPreference(Model):
    user = models.ForeignKey('user_management.User', on_delete=models.CASCADE, null=True, blank=True)
    job_preference = models.CharField(
        max_length=255,
        choices=JOB_TYPE_CHOICES,
        default='none'
    )
    status = models.BooleanField(default=True, blank=True)
