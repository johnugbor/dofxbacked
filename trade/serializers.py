from rest_framework import serializers
from .models import Wallet, Transaction, TradeTransaction, Asset


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'balance', 'user_id')


class TradeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeTransaction
        fields = ('id','open_price', 'asset_name', 'asset_volume', 'trade_type', 'cost', 'profit', 'stop_loss_value',
                  'stop_loss_price', 'is_trade_open', 'close_time', 'symbol')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'transaction_type', 'transaction_status', 'wallet', 'timestamp_created')


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            "name", "symbol", "chart_symbol", "price", "bid", "ask", "currency", "img", "group", "popular", "change",
            "spread_diff", "digits", "description", "contract_size", "instrument", "volume_min", "volume_max",
            "volume_step", "tick_size", "tick_value", "margin_initial", "mode", "profit_mode", "market_state",
            "stops_level", "lots_currency", "display_name", "mover"
        )
