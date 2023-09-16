from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from lit_auth.forms import OtpAuthenticationForm
from lit_auth.models import User, OtpCode
from lit_auth.permissions import UserPermission
from lit_auth.serializers import UserSerializer, OtpCodeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission, ]


class GetOTPView(CreateAPIView):
    serializer_class = OtpCodeSerializer
    queryset = OtpCode.objects.all()
    permission_classes = [AllowAny, ]


class OtpLoginView(LoginView):
    form_class = OtpAuthenticationForm
    template_name = "lit_auth/login.html"

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        elif self.request.user:
            return reverse('user-detail', args=[self.request.user.id])
        else:
            return '/'
