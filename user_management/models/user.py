from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)


class UserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, is_staff=False, is_superuser=False, is_active=True):
        if not email:
            raise ValueError('Users must have a email address')
        if not password:
            raise ValueError('Users must have a password')

        user_obj = self.model(
            email=self.normalize_email(email),
            name=name,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user_obj.active = is_active
        user_obj.set_password(password)
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, name=None, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, name=None, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password,
            is_staff=True,
            is_superuser=True,
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)

    is_staff = models.BooleanField(default=False, blank=True)
    status = models.CharField(max_length=10, blank=True, choices=(
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ), default='active')
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return "%s" % self.name
