from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.views import View

# /account_signup
class Index(View):
    def get(self, request, *arg, **kwargs):
        if User.is_authenticated:
            return redirect( '/accounts/login/')
        else:
            return redirect('/accounts/login/')