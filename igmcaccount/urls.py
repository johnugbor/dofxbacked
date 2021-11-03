from django.urls import path, include, re_path

from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import PasswordResetConfirmView
from igmcaccount.views import EmailConfirmationView

from drf_jwt_2fa.views import obtain_auth_token, obtain_code_token

urlpatterns = [
    path('account/', include('dj_rest_auth.urls')),
    
    
    path('account/registration/', include('dj_rest_auth.registration.urls'), name='registration'),
    re_path(r'^account/account-confirm-email/(?P<key>[-:\w]+)/$', EmailConfirmationView.as_view(), name='account_confirm_email'),
    path('account/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('password-reset/confirm/<slug:uidb64>/<slug:token>/',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'
    ),
     re_path(r'^login/', obtain_code_token),
     re_path(r'^two-fa/', obtain_auth_token),
    
] 
