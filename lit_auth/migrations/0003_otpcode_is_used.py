# Generated by Django 4.2.5 on 2023-09-16 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lit_auth', '0002_otpcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpcode',
            name='is_used',
            field=models.BooleanField(default=False, verbose_name='OTP is used'),
        ),
    ]