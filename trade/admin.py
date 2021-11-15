from django.contrib import admin

from .models import Wallet, Transaction

class WalletAdmin(admin.ModelAdmin):
	list_display = ('id','balance','user_id',)

admin.site.register(Wallet,WalletAdmin)
