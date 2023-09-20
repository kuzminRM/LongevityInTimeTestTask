from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework import routers

from lit_auth.views import UserViewSet, GetOTPView, OtpLoginView

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('otp/', GetOTPView.as_view(), name='login_get_otp'),
    path('login/', OtpLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
