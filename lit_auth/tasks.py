from celery import shared_task
from django.core.mail import send_mail

from lit_auth.models import OtpCode


@shared_task
def send_otp_mail(otp_obj_id: int):
    otp_obj = OtpCode.objects.get(id=otp_obj_id)

    result: int = send_mail(
        'LIT_TT: Auth code',
        f'Your authorization code is: {otp_obj.otp}',
        None, [otp_obj.email]
    )
    if result == 1:
        otp_obj.status = OtpCode.Status.OK
    else:
        otp_obj.status = OtpCode.Status.ERROR
    otp_obj.save(update_fields=['status'])
