from django.utils.translation import gettext_lazy as _
from django.db import models
from igmcaccount.models import User
# Create your models here.

class Wallet(models.Model):
	balance = models.FloatField()
	user_id = models.OneToOneField(User, on_delete=models.CASCADE)

class Transaction(models.Model):
	class TransactionType(models.TextChoices):
		BUY = 'BUY',_('Buy')
		SELL = 'SELL',_('Sell')
		DEPOSIT = 'DEPO',_('Deposit')
		WITHDRAWAL = 'WITHD',_('Withdrawal')

	amount = models.FloatField()
	transaction_type =models.CharField(max_length=5,choices=TransactionType.choices,default=TransactionType.WITHDRAWAL,)
	wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)