from rest_framework  import serializers
from .models import Wallet, Transaction,TradeTransaction

class WalletSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = ('id','balance','user_id')
class TradeTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TradeTransaction
		fields =('id','open_price','asset_name','asset_volume','trade_type','cost','profit','stop_loss_value','stop_loss_price','is_trade_open','close_time','wallet','user','symbol')
class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ('id','amount','transaction_type','transaction_status','wallet','timestamp_created')