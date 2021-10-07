from django.contrib import admin
from .models import detail, otp_verify

# Register your models here.


# admin.site.register(user_details)
admin.site.register(detail)
admin.site.register(otp_verify)
# admin.site.register(user_signed_up)