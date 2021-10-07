from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('Loginauth/', views.Login, name='Loginauth'),
    path('LogOutAuth/', views.Logout, name='LogOutAuth'),
    path('forgotAuth/', views.ForgotAuth, name='forgotAuth')
]
