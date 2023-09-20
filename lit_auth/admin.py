from django.contrib import admin
from lit_auth.models import User, OtpCode

models = [User, OtpCode]

for model in models:
    admin.site.register(model)
