from random import randint
from django.conf import settings
from django.core.mail import send_mail


def rounding(follower):
    if 1000 <= follower < 1000000:
        if follower % 1000 == 0:
            follower = int(follower) // 1000
        else:
            follower = int(follower) / 1000
        follower = round(follower, 2)
        follower = str(follower) + 'K'
    elif follower >= 1000000:
        if follower % 1000000 == 0:
            follower = int(follower) // 1000000
        else:
            follower = int(follower) / 1000000
        follower = round(follower, 2)
        follower = str(follower) + 'M'
    return follower


def sending_mail(email):
    star = 0
    for i in range(len(email)):
        if email[i] == "@":
            break
        else:
            star += 1

    otp = randint(100000, 1000000)
    subject = "Hustlers account password reset"
    message = """
Hustlers account
Password reset code

Please use this code to reset the password for the Hustlers account """ + email[:3] + str("*" * (star - 3)) + email[star:] + """
Here is your code: """ + str(otp) + """

1. Do not share your credentials or otp with anyone on call, email or sms.
2. Our Community never asks you for your credentials or otp.
3. Always create a strong password and keep different passwords for different websites.

Thanks,
The Hustler account team
    """
    # print(subject)
    # print(message)

    recipient_list = [email]
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)
    return otp
