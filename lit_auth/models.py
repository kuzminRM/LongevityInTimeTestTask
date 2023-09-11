from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import validate_email


class CustomUserManager(UserManager):

    def _get_email(self, email: str):
        validate_email(email)
        return self.normalize_email(email)

    def _create_user(
            self,
            email: str,
            password: str,
            commit: bool,
            is_staff: bool = False,
            is_superuser: bool = False,
            username=None,
    ):
        email = self._get_email(email)

        user = User(email=email, username=username or email, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)

        if commit:
            user.save()

        return user

    def create_superuser(self, email: str, password: str, commit: bool = True):
        return self._create_user(email, password, is_staff=True, is_superuser=True, commit=commit)

    def create_user(self, email: str, password: str, commit: bool = True):
        return self._create_user(email, password, commit=commit)

    def create(self):
        pass


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email address')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"
