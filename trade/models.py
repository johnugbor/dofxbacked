from decimal import Decimal

from django.utils.translation import gettext_lazy as _
from django.db import models, transaction, IntegrityError
from .errors import *

from base.models import BaseModel
from igmcaccount.models import User


# from django.contrib.auth.models import User as Users

# Create your models here.


class Wallet(BaseModel):
    balance = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL,
                                related_name='wallet')

    def get_queryset(self):

        return self.__class__.objects.filter(id=self.id)

    # @classmethod
    # def create(cls, user):
    #     newwallet = cls(user=user)
    #     newwallet.create(user=user)
    #     return newwallet.balance

    @transaction.atomic()
    def deposit(self, amount, email):
        """ Deposit `amount` to wallet.
        """
        amount = Decimal(amount)

        obj = self.get_queryset().select_for_update().get()
        obj.debit_withdraw_transaction.create(
            amount=amount,
            transaction_type='DEPO',
            transaction_status='COMPLETED',
            email=email,

        )
        obj.balance += amount
        obj.save()

    @transaction.atomic()
    def withdraw(self, amount, email):

        """ Withdraw `amount` to wallet.

        """

        amount = Decimal(amount)

        obj = self.get_queryset().select_for_update().get()
        if amount > obj.balance:
            raise InsufficientFunds()
        obj.debit_withdraw_transaction.create(
            amount=amount,
            transaction_type='WITHD',
            transaction_status='PROCESSING',
            email=email,

        )
        obj.balance -= amount
        obj.save()

    @transaction.atomic()
    def tradeclosedeposit(self, amount, email):
        """ Deposit `amount` to wallet.
        """
        amount = Decimal(amount)

        obj = self.get_queryset().select_for_update().get()
        obj.debit_withdraw_transaction.create(
            amount=amount,
            transaction_type='CLOSE',
            transaction_status='COMPLETED',
            email=email,

        )
        obj.balance += amount
        obj.save()

    @transaction.atomic()
    def openbuy(self, asset_name, asset_volume, useremail, cost, open_price, profit, stop_loss_value, stop_loss_price,
                symbol, leverage):
        cost = Decimal(cost)
        open_price = Decimal(open_price)
        stop_loss_value = Decimal(stop_loss_value)
        stop_loss_price = Decimal(stop_loss_price)

        obj = self.get_queryset().select_for_update().get()
        if cost > obj.balance:
            raise InsufficientFunds()
        obj.tradetransaction.create(

            asset_name=asset_name,
            asset_volume=asset_volume,
            trade_type='BUY',
            cost=cost,
            open_price=open_price,
            current_price=open_price,
            profit=profit,
            stop_loss_value=stop_loss_value,
            stop_loss_price=stop_loss_price,
            symbol=symbol,
            user=useremail,
            leverage=leverage,

        )
        obj.balance -= cost
        obj.save()

    @transaction.atomic()
    def opensell(self, asset_name, asset_volume, useremail, cost, open_price, profit, stop_loss_value, stop_loss_price,
                 symbol, leverage):
        cost = Decimal(cost)
        open_price = Decimal(open_price)
        stop_loss_value = Decimal(stop_loss_value)
        stop_loss_price = Decimal(stop_loss_price)

        obj = self.get_queryset().select_for_update().get()
        balance = obj.balance
        if cost > obj.balance:
            raise InsufficientFunds(balance, cost)
        obj.tradetransaction.create(

            asset_name=asset_name,
            asset_volume=asset_volume,
            trade_type='SELL',
            cost=cost,
            open_price=open_price,
            current_price=open_price,
            profit=profit,
            stop_loss_value=stop_loss_value,
            stop_loss_price=stop_loss_price,
            symbol=symbol,
            user=useremail,
            leverage=leverage,

        )
        obj.balance -= cost
        obj.save()


# class UserProxy(User):
#
#     class Meta:
#         proxy = True
#
#     def save(self):
#         Wallet.objects.get_or_create(user=self.id)
#         Wallet.save()


class Transaction(BaseModel):
    class TransactionType(models.TextChoices):
        BUY = 'BUY', _('Buy')
        CLOSE = 'CLOSE', _('Trade Close')
        DEPOSIT = 'DEPO', _('Deposit')
        WITHDRAWAL = 'WITHD', _('Withdrawal')

    class TransactionStatus(models.TextChoices):
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    amount = models.DecimalField(
        _('Tranaction Amount'), max_digits=10, decimal_places=2, default=0
    )
    transaction_type = models.CharField(max_length=5, choices=TransactionType.choices,
                                        default=TransactionType.WITHDRAWAL, )
    transaction_status = models.CharField(max_length=10, choices=TransactionStatus.choices,
                                          default=TransactionStatus.PROCESSING)
    email = models.CharField(max_length=555, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='debit_withdraw_transaction')

    def process_withdraw(self, request, pk):
        user = self.request.user
        if not user.request.is_superuser:
            raise IntegrityError("You don't have access right")
        obj = self.get_queryset().select_for_update().get()
        obj.create(
            id=pk,
            transaction_status="COMPLETED")
        obj.save()


class Asset(models.Model):
    name = models.CharField(max_length=52)
    symbol = models.CharField(primary_key=True, max_length=22)
    chart_symbol = models.CharField(max_length=2222)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ask = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3)
    img = models.CharField(max_length=23445)
    group = models.CharField(max_length=70)
    popular = models.BooleanField(default=False)
    change = models.DecimalField(max_digits=4, decimal_places=3, default=0)
    spread_diff = models.IntegerField(default=0)
    digits = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True, default="Enter description...")
    contract_size = models.DecimalField(default=0, decimal_places=2, max_digits=100)
    instrument = models.IntegerField(default=0)
    volume_min = models.IntegerField(default=1)
    volume_max = models.IntegerField(default=3000)
    volume_step = models.IntegerField(default=1)
    tick_size = models.IntegerField(default=0)
    tick_value = models.IntegerField(default=0)
    margin_initial = models.IntegerField(default=0)
    mode = models.IntegerField(default=0)
    profit_mode = models.IntegerField(default=0)
    market_state = models.IntegerField(default=0)
    stops_level = models.IntegerField(default=0)
    lots_currency = models.CharField(default="USD", max_length=6)
    display_name = models.CharField(max_length=220)
    mover = models.IntegerField(default=0)


class TradeTransaction(models.Model):
    class TradeType(models.TextChoices):
        BUY = ('BUY', _('Buy'))
        SELL = ('SELL', _('Sell'))

    open_time = models.DateTimeField(auto_now=True)
    asset_name = models.CharField(max_length=32)
    asset_volume = models.IntegerField(default=0)
    trade_type = models.CharField(max_length=4, choices=TradeType.choices, default=TradeType.BUY
                                  )
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    open_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leverage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stop_loss_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stop_loss_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_trade_open = models.BooleanField(default=True)
    close_time = models.DateTimeField(null=True, blank=True)
    wallet = models.ForeignKey(Wallet, null=True, on_delete=models.SET_NULL, related_name='tradetransaction')
    user = models.CharField(max_length=555, null=True)
    symbol = models.CharField(max_length=32, null=True)
