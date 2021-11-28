from django.shortcuts import render
from rest_framework import viewsets, status,exceptions
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date, timedelta, datetime, time
from .serializers import WalletSerializer,TransactionSerializer
from .models import Wallet, Transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from base.renderers import custom_response_renderer
# Create your views here.
class CheckBalance(APIView):
	serializer_class = WalletSerializer
	#queryset  = Wallet.objects.all()
	permission_classes = [IsAuthenticated]

	def post(self, request):
		myuser =self.request.user
		data ={}
		if myuser.is_superuser:

			data = Wallet.objects.all()
			print(data)


		else:


			data = WalletSerializer(Wallet.objects.filter(user_id=myuser)).data
		return custom_response_renderer(data=data,status=True,status_code=status.HTTP_200_OK)


class DepositAmount(APIView):
	serializer_class = WalletSerializer
	#queryset  = Wallet.objects.all()
	

	permission_classes = [IsAuthenticated,IsAdminUser]

	def post(self, request):
		

		amount = request.data.get('amount', None)

		success, error_msg, data = True, None, {}

		if ( not amount ) or (amount <=0):
			success = False
			error_msg = "Invalid amount."
		if success:
			wallet = request.user.get_wallet()

			if not wallet:
				success = False
				error_msg = "Wallet does  not exist for user."
		if success:
			with transaction.atomic():
				wallet.deposit(amount)
			data = WalletSerializer(wallet).data 
		return Response( 
			data= data,
			error_msg=error_msg,
			status=success,
			status_code= status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
			)

class WithdrawAmount(APIView):

	serializer_class = WalletSerializer
	#queryset  = Wallet.objects.all()
	permission_classes = [IsAuthenticated]

	def post(self, request):
		

		amount = request.data.get('amount', None)
		success, error_msg, data = True, None, {}

		if (not amount) or (amount <= 0):

			success = False
			error_msg = "Invalid amount."
		if success:
			wallet = request.user.get_wallet()

			if not wallet:
				success = False
				error_msg = "Wallet does not exist for user."

		if success:
			email = request.user.email
			wallet.withdraw(amount,email)
			data = WalletSerializer(wallet).data

		return custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )
class ListTransactions(APIView):
    """ API to list all money transactions.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated,]
    

def post(self, request, pk):


		data ={}
		if request.user.is_staff:
			transactions = Transaction.objects.filter(
                id=pk).order_by('-timestamp_created')
			data = transactions
		else:
			wallet = request.user.get_wallet()
			if not wallet:
				raise exceptions.APIException(
                    "Wallet not found.")
			if wallet.id != pk:
				raise exceptions.PermissionDenied()

			transactions = wallet.transaction_set.order_by(
                '-timestamp_created')
			data = transactions

        

			return custom_response_renderer(
            data=data, status=True, status_code=status.HTTP_200_OK)
class ProcessWithdrawal(APIView):
    """ API to process withdraw transactions.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    
def post(self, request):
	pk = request.data.get('pk', None)
	success, error_msg, data = True, None, {}


	data ={}
	if request.user.is_staff:
		transactions = Transaction.objects.filter(
    id=pk)
		transactions.process_withdraw(pk)
		data =TransactionSerializer(transactions).data
		return custom_response_renderer(
		data=data, status=True, status_code=status.HTTP_200_OK)
	else:
		return





