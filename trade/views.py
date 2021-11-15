from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date, timedelta, datetime, time
from .serializers import WalletSerializer,TransactionSerializer
from .models import Wallet, Transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
# Create your views here.
class WalletView(viewsets.ModelViewSet):
	serializer_class = WalletSerializer
	#queryset  = Wallet.objects.all()
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		myuser =self.request.user
		if myuser.is_superuser:

			return Wallet.objects.all()
		else:


			return Wallet.objects.filter(user_id=myuser)