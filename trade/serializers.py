from rest_framework  import serializers
from .models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = ('id','balance','user_id')
class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ('id','amount','transaction_type','wallet_id')