from decimal import Decimal

from django.utils.translation import gettext_lazy as _
from django.db import models, transaction,IntegrityError

from base.models import BaseModel
from igmcaccount.models import User
# Create your models here.


class Wallet(BaseModel):
	balance = models.DecimalField(_('Wallet Balance'), max_digits=10, decimal_places=2, default=0)
	user = models.OneToOneField(User,null=True, on_delete=models.SET_NULL,
        related_name='wallet')

	def get_queryset(self):
		
	 	return self.__class__.objects.filter(id=self.id)

	@transaction.atomic()
	def deposit(self, amount):
		""" Deposit `amount` to wallet.
        """
		amount = Decimal(amount)

		obj = self.get_queryset().select_for_update().get()
		obj.transaction_set.create(
            amount=amount,
            transaction_type='DEPO',
            transaction_status='COMPLETED',
            
        )
		obj.balance += amount
		obj.save()

	@transaction.atomic()
	def withdraw(self, amount,email):

		""" Withdraw `amount` to wallet.

        """
		
		amount = Decimal(amount)
		

		obj = self.get_queryset().select_for_update().get()
		if amount > obj.balance:
			raise errors.InsufficientFunds()
		obj.transaction_set.create(
            amount=amount,
            transaction_type='WITHD',
            transaction_status='PROCESSING',
            email=email,
            
        )
		obj.balance -= amount
		obj.save()



class Transaction(BaseModel):
        

	class TransactionType(models.TextChoices):
		BUY = 'BUY',_('Buy')
		SELL = 'SELL',_('Sell')
		DEPOSIT = 'DEPO',_('Deposit')
		WITHDRAWAL = 'WITHD',_('Withdrawal')

	class TransactionStatus(models.TextChoices):
		PROCESSING = 'PROCESSING',_('Processing')
		COMPLETED  = 'COMPLETED',_('Completed')
		CANCELLED = 'CANCELLED',_('Cancelled')

	amount = models.DecimalField(
        _('Tranaction Amount'), max_digits=10, decimal_places=2, default=0
    )
	transaction_type =models.CharField(max_length=5,choices=TransactionType.choices,default=TransactionType.WITHDRAWAL,)
	transaction_status = models.CharField(max_length=10, choices=TransactionStatus.choices,default=TransactionStatus.PROCESSING)
	email = models.CharField(max_length=555, null=True)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,related_name='debit_withdraw_transaction')



	def process_withdraw(self,request,pk):

		user = self.request.user
		if not user.request.is_superuser:
			raise IntegrityError("You don't have access right")
		obj = self.get_queryset().select_for_update().get()
		obj.create(
			id=pk,
			transaction_status="COMPLETED")
		obj.save()
class TradeTransaction(models.Model):

	class TradeType(models.TextChoices):
		BUY =('BUY',_('Buy'))
		SELL =('SELL',_('Sell'))

	class TradeStatusType(models.TextChoices):
		OPEN = ('OPEN',_('Open'))
		CLOSE = ('CLOSE',_('Close'))
	open_time = models.DateTimeField(auto_now=True)
	asset_name = models.CharField(max_length=32)
	asset_volume =models.IntegerField(default=0)
	trade_type =models.CharField(max_length=4, choices=TradeType.choices,default=TradeType.BUY
		)
	cost =models.DecimalField(max_digits=10,decimal_places=2,default=0)
	open_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
	profit=models.DecimalField(max_digits=10,decimal_places=2,default=0)
	stop_loss_value=models.DecimalField(max_digits=10,decimal_places=2,default=0)
	stop_loss_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
	current_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
	trade_status = models.CharField(max_length=5, choices=TradeStatusType.choices,default=TradeStatusType.OPEN)
	close_time = models.DateTimeField(null=True,blank=True)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,related_name='trade_open_close')
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='trade_transaction')












