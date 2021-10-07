import time

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import detail, otp_verify
from . import functions as fn

# Create your views here.
user_info = {
    'username': ''
}


# user
# detail

def index(request):
    if request.user.is_authenticated:

        if detail.objects.filter(email=request.user).exists():
            details = detail.objects.filter(email=request.user)
            details = list(details.values())
            details = details[0]

            details['follower'] = fn.rounding(details['follower'])
            details['following'] = fn.rounding(details['following'])
            details['post'] = fn.rounding(details['post'])

            description = details['description'].split(' ')
            details['description'] = ' '.join(map(str, description[:20])) + '. . . .'

            details['pic_url'] = '/static/' + details['pic_url']

            return render(request, 'index.html', details)
        else:
            return render(request, 'description.html')
    else:
        return redirect('Loginauth')


def Login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = authenticate(request, username=email, password=password)
            except:
                return JsonResponse({"status": "Server Error"})

            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'Success'})
            else:
                return JsonResponse({"status": "Invalid Credentials"})

        else:
            return render(request, 'Login.html')


def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('Loginauth')


def ForgotAuth(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            try:
                if request.POST.get('type') == 'email-form':
                    email = request.POST.get('email')
                    if User.objects.filter(username=email).exists():
                        otp = fn.sending_mail(email)
                        current_time = int(time.time())
                        after_time = current_time+900
                        otp_check = otp_verify(email=email, otp=otp, time_now=current_time, time_after=after_time)
                        otp_check.save()
                        return JsonResponse({'status': 'Success1'})
                    else:
                        return JsonResponse({'status': 'No such user exist in database'})
                elif request.POST.get('type') == 'otp-form':
                    email = request.POST.get('email')
                    otp = request.POST.get('otp')

                    if otp_verify.objects.filter(email=email, otp=otp).exists():
                        check = otp_verify.objects.filter(email=email, otp=otp)
                        check = list(check.values())
                        check = check[0]
                        time_now = int(time.time())
                        if int(check['time_now']) < time_now <= int(check['time_after']):
                            return JsonResponse({'status': 'Success2'})
                        else:
                            return JsonResponse({'status': 'OTP Expired'})
                    else:
                        return JsonResponse({'status': 'Invalid OTP'})
                elif request.POST.get('type') == 'forgot-form':
                    email = request.POST.get('email')
                    password = request.POST.get('password')
                    otp = request.POST.get('otp')

                    if otp_verify.objects.filter(email=email, otp=otp).exists():
                        user_obj = User.objects.get(username=email)
                        user_obj.set_password(password)
                        user_obj.save()
                        print(user_obj)
                        deleting = otp_verify.objects.filter(email=email)
                        for i in deleting:
                            checking = otp_verify(id=i.id)
                            checking.delete()
                        return JsonResponse({'status': 'Success3'})
                    else:
                        return JsonResponse({'status': 'Suspicious activity founded'})
            except Exception as e:
                return JsonResponse({'status': str(e)})
        else:
            return render(request, 'forgotAuth.html')


