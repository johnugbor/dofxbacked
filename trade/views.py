from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status, exceptions
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date, timedelta, datetime, time
from .serializers import WalletSerializer, TransactionSerializer, TradeTransactionSerializer, AssetSerializer
from .models import Wallet, Transaction, TradeTransaction, Asset
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from base.renderers import custom_response_renderer
from django.db.models import Sum
from django.shortcuts import get_object_or_404

# Create your views here.
class CheckBalance(APIView):
    serializer_class = WalletSerializer
    # queryset  = Wallet.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        myuser = self.request.user
        serilizeddata = {}
        if myuser:

            data = Wallet.objects.filter(user=myuser)
            print(myuser)
            print(data)
            serilizeddata = WalletSerializer(data, many=True).data[0]



        else:
            data = Wallet.objects.get(user=myuser)
            print(myuser)
            print(data)

            serilizeddata = WalletSerializer(data).data
        return custom_response_renderer(data=serilizeddata, status=True, status_code=status.HTTP_200_OK)


class DepositAmount(APIView):
    serializer_class = WalletSerializer
    # queryset  = Wallet.objects.all()

    permission_classes = [IsAuthenticated, IsAdminUser]

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
                error_msg = "Wallet does  not exist for user."
        if success:
            email = request.user.email
            with transaction.atomic():
                wallet.deposit(amount, email)
            data = WalletSerializer(wallet).data
        return Response(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        )


def post(request):
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
        wallet.withdraw(amount, email)
        data = WalletSerializer(wallet).data

    return custom_response_renderer(
        data=data,
        error_msg=error_msg,
        status=success,
        status_code=status.HTTP_200_OK if success else
        status.HTTP_400_BAD_REQUEST
    )


class WithdrawAmount(APIView):
    serializer_class = WalletSerializer
    # queryset  = Wallet.objects.all()
    permission_classes = [IsAuthenticated]


class BuyOrder(APIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        asset_symbol = request.data.get('symbol', None)
        asset_volume = request.data.get('volume')
        stop_loss_value = request.data.get('sl')
        leverage = 1

        success, error_msg, data = True, None, {}

        if (not asset_volume) or (asset_volume <= 0):
            success = False,
            error_msg = "Invalid asset volume."
        if (not stop_loss_value) or (stop_loss_value <= 0):
            success = False,
            error_msg = "Invalid stop loss value."
        trade_asset = Asset.objects.get(symbol=asset_symbol)

        if (not trade_asset):
            success = False,
            error_msg = "Invalid asset."

        if success:
            wallet = request.user.get_wallet()

            if not wallet:
                success = False
                error_msg = "Wallet does not exist for user."

        if success:
            useremail = request.user.email
            open_price = trade_asset.price
            current_price = trade_asset.price
            stop_loss_value = stop_loss_value
            asset_name = trade_asset.name
            asset_volume = asset_volume
            symbol = asset_symbol
            profit = 0

            cost = asset_volume * open_price
            stop_loss_price = (asset_volume * open_price - stop_loss_value) / open_price
        if wallet.balance < cost:
            success = False
            error_msg = "Insufficient balance"
        if success:

            wallet.openbuy(asset_name, asset_volume, useremail, cost, open_price, profit, stop_loss_value,
                           stop_loss_price, symbol, leverage)

        return custom_response_renderer(

            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )


class SellOrder(APIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        asset_symbol = request.data.get('symbol', None)
        asset_volume = request.data.get('volume')
        stop_loss_value = request.data.get('sl')
        leverage = 1

        success, error_msg, data = True, None, {}

        if (not asset_volume) or (asset_volume <= 0):
            success = False,
            error_msg = "Invalid asset volume."
        if (not stop_loss_value) or (stop_loss_value <= 0):
            success = False,
            error_msg = "Invalid stop loss value."
        trade_asset = Asset.objects.get(symbol=asset_symbol)

        if (not trade_asset):
            success = False,
            error_msg = "Invalid asset."

        if success:
            wallet = request.user.get_wallet()

        if not wallet:
            success = False
            error_msg = "Wallet does not exist for user."

        if success:
            useremail = request.user.email
            open_price = trade_asset.price
            current_price = trade_asset.price
            stop_loss_value = stop_loss_value
            asset_name = trade_asset.name
            asset_volume = asset_volume
            symbol = asset_symbol
            profit = 0

            cost = asset_volume * open_price
            stop_loss_price = (asset_volume * open_price - stop_loss_value) / open_price
        if wallet.balance < cost:
            success = False
            error_msg = "Insufficient balance"
        if success:

            wallet.opensell(asset_name, asset_volume, useremail, cost, open_price, profit, stop_loss_value,
                            stop_loss_price, symbol, leverage)

        return custom_response_renderer(

            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )


class OpenPosition(APIView):
    serializer_class = TradeTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user.email
        openpositions = TradeTransaction.objects.filter(is_trade_open=True, user=user)

        success, error_msg, data = True, None, {}

        if (not openpositions):
            success = False,
            error_msg = "User doesn't have an open position"
        if success:
            data = TradeTransactionSerializer(openpositions, many=True).data
        return custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )


class ClosedPosition(APIView):
    serializer_class = TradeTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user.email
        openpositions = TradeTransaction.objects.filter(is_trade_open=False, user=user)

        success, error_msg, data = True, None, {}

        if (not openpositions):
            success = False,
            error_msg = "User doesn't have an closed position"
        if success:
            data = TradeTransactionSerializer(openpositions, many=True).data
        return custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )


# for closing a position

class ClosePosition(APIView):
    """ API to close a position on button click.
	"""
    serializer_class = TradeTransactionSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):

        pk = request.data.get('transaction_id')
        user = self.request.user.email

        success, error_msg, data = True, None, {}
        if (not pk):
            success = False,
            error_msg = "transaction id doesn't exist."

        if success:
            wallet = request.user.get_wallet()

            if not wallet:
                success = False
                error_msg = "Wallet does not exist for user."

        if success:

            tradedata = get_object_or_404(TradeTransaction,id=pk,user=user)

            if not tradedata:

                success = False,
                error_msg = "Sorry you don't have the right to close this trade."


        if success:

            if tradedata.is_trade_open == False:
                print(tradedata.is_trade_open)
                success = False,
                error_msg = "The trade has been closed."
            if success:
                if tradedata.trade_type == 'BUY':
                    profit = (tradedata.asset_volume * tradedata.current_price - tradedata.cost) * tradedata.leverage
                elif tradedata.trade_type == 'SELL':
                    profit = (tradedata.asset_volume * tradedata.current_price - tradedata.cost) * tradedata.leverage * -1
                tradedata.is_trade_open = False
                tradedata.close_time = datetime.now()
                tradedata.profit = profit
                wallet.tradeclosedeposit(profit, user)
                tradedata.save()
                serializeddata = TradeTransactionSerializer(tradedata)
                data =serializeddata.data
                print(serializeddata)

        return  custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else
            status.HTTP_400_BAD_REQUEST
        )



class FinancePanel(APIView):
    serializer_class = TradeTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = self.request.user.email
        success, error_msg, data = True, None, {}
        finance_data = TradeTransaction.objects.filter(is_trade_open=True, user=user)
        if (not finance_data):
            success = False,
            error_msg = "You don't have trade data."
        if success:
            finance_value = ['cost', 'profit', 'stop_loss_value']
            summed_usedmargin = finance_data.aggregate(Sum('cost'))['cost__sum']
            summed_profit = finance_data.aggregate(Sum('profit'))['profit__sum']
            summed_stoploss = finance_data.aggregate(Sum('stop_loss_value'))['stop_loss_value__sum']

            data = TradeTransactionSerializer(finance_data, many=True).data

        return Response({
            'data': {'usedmargin': summed_usedmargin if summed_usedmargin else 0,
                     'profit': summed_profit if summed_profit else 0,
                     'stoploss': summed_stoploss if summed_stoploss else 0, }, })


class AssetView(APIView):
    serializer_class = AssetSerializer

    def get(self, request):
        assets = Asset.objects.all()
        success, error_msg, data = True, None, {}
        if not assets:
            success = False
            error_msg = "There is no asset item available"
        if success:
            data = AssetSerializer(assets, many=True).data
        return custom_response_renderer(
            data=data,
            error_msg=error_msg,
            status=success,
            status_code=status.HTTP_200_OK if success else status.HTTP_204_NO_CONTENT

        )


class ListTransactions(APIView):
    """ API to list all money transactions.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, ]


def post(self, request, pk):
    data = {}
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
    permission_classes = [IsAuthenticated, IsAdminUser]


def post(self, request):
    pk = request.data.get('pk', None)
    success, error_msg, data = True, None, {}

    data = {}
    if request.user.is_staff:
        transactions = Transaction.objects.filter(
            id=pk)
        transactions.process_withdraw(pk)
        data = TransactionSerializer(transactions).data
        return custom_response_renderer(
            data=data, status=True, status_code=status.HTTP_200_OK)
    else:
        return
