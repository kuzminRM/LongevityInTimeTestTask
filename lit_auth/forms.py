from django.contrib.auth.forms import AuthenticationForm
from django import forms

from lit_auth.models import OtpCode


class OtpAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(label="OTP code")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['otp'].widget.attrs.update({"autocomplete": "off"})

    def clean(self):
        # validate email & password
        cleaned_data = super(OtpAuthenticationForm, self).clean()

        # validate OTP
        if cleaned_data.get('username') and cleaned_data.get('otp'):
            otp_is_valid, otp_msg = OtpCode.validate_otp(cleaned_data['username'], cleaned_data['otp'])
            if not otp_is_valid:
                self.add_error('otp', otp_msg)

        return cleaned_data
