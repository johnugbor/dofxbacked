from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from rest_framework import status, viewsets, parsers
from rest_framework.response import Response
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.registration.views import RegisterView

import igmcaccount.serializers as serializers
import igmcaccount.models as models
from .serializers import CustomRegisterSerializer
class AccountRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class EmailConfirmationView(VerifyEmailView):

    '''Email Confirmation view'''
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        user = confirmation.email_address.user
        if user.is_verified:
            return Response(
                {'detail':_('Email already verified')},
                status = status.HTTP_200_OK
            )
            #return Response({'detail': _('Email already verified')}, status=status.HTTP_200_OK)
        else:
            user.is_verified = True
            user.save()
            return Response(
                {'detail': _(user.username+ ' Mail Successfully Verified')}, 
                status=status.HTTP_200_OK
            )