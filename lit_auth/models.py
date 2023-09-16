import datetime
import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import validate_email
from django.utils import timezone


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


class OtpCode(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pend', 'In progress'
        OK = 'ok', 'Sent to recipient'
        ERROR = 'err', 'Error'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    email = models.EmailField(verbose_name='Email address')
    otp = models.CharField(max_length=6, verbose_name='OTP code')
    is_used = models.BooleanField(verbose_name='OTP is used', default=False)
    status = models.CharField(max_length=4, choices=Status.choices,
                              default=Status.PENDING, verbose_name='Code send status')

    @classmethod
    def send_auth_otp(cls, email: str) -> 'OtpCode':
        # probably is's would be better to relocate this "class-functions" to the separate file
        # to avoid local imports like this and make models.py more readable when we add more models
        from lit_auth.tasks import send_otp_mail
        otp_code: str = cls.__generate_otp_code()
        otp_obj: OtpCode = OtpCode.objects.create(email=email, otp=otp_code)
        send_otp_mail.delay(otp_obj.id)
        return otp_obj

    @staticmethod
    def __generate_otp_code() -> str:
        return str(random.randint(0, 999_999)).rjust(6, '0')

    @staticmethod
    def validate_otp(email: str, otp: str) -> tuple[bool, str]:
        """
        If OTP is valid for this email it would return tuple (True, 'Success') and deactivates it,
        otherwise (False, <msg>), where <msg> is error reason
        """
        otp_obj: OtpCode = OtpCode.objects.filter(email=email.lower()).latest('created_at')
        if not otp_obj:
            return False, 'Wrong email. Email not found'
        elif otp_obj.otp == otp:
            if otp_obj.is_used:
                return False, 'OTP code has been already used'
            elif otp_obj.created_at + datetime.timedelta(minutes=5) >= timezone.now():
                otp_obj.is_used = True
                otp_obj.save(update_fields=['is_used'])
                return True, 'Success'
            else:
                return False, 'OTP code has expired'
        else:
            return False, 'Wrong OTP code'

    def __str__(self):
        return f"{self.email} {self.created_at}"
