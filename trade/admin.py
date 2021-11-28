from django.contrib import admin

from .models import Wallet, Transaction,TradeTransaction

class WalletAdmin(admin.ModelAdmin):
	list_display = ('id','balance','user_id',)

class TransactionAdmin(admin.ModelAdmin):
	list_display = ('id','amount','transaction_type','transaction_status','email','wallet')

class TradeTransactionAdmin(admin.ModelAdmin):
	list_display = ('id','open_time', 'asset_name', 'asset_volume', 'trade_type', 'cost', 'open_price', 'profit', 'stop_loss_value', 'stop_loss_price', 'current_price',
'trade_status','close_time', 'wallet', 'user',)

admin.site.register(Wallet,WalletAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(TradeTransaction,TradeTransactionAdmin)