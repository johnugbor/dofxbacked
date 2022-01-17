import asyncio
import websocket
import json
from .models import Asset, TradeTransaction
from django_bulk_update.helper import bulk_update


def on_message(ws, message):
    data = json.loads(message)
    item = Asset.objects.all()
    trade= TradeTransaction.objects.all()
    #print(data)

    print(data["data"])
    for i in range(len(item)):
        # get the symbol
        asset_item_symbol = item[i].symbol
        for j in range(len(data)):
            if data["data"][j]['s'] == asset_item_symbol:
                item[i].price = data["data"][j]["p"]

    bulk_update(item, update_fields=['price'])



# Consider using django-bulk-update found here on GitHub.
#
# Install: pip install django-bulk-update
#
# Implement: (code taken directly from projects ReadMe file)
#
# from bulk_update.helper import bulk_update
#
# random_names = ['Walter', 'The Dude', 'Donny', 'Jesus']
# people = Person.objects.all()
#
# for person in people:
#     r = random.randrange(4)
#     person.name = random_names[r]
#
# bulk_update(people)  # updates all columns using the default d


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"ABNB"}')
    ws.send('{"type":"subscribe","symbol":"BA"}')
    ws.send('{"type":"subscribe","symbol":"BABA"}')

    ws.send('{"type":"subscribe","symbol":"MA"}')
    ws.send('{"type":"subscribe","symbol":"MSFT"}')
    ws.send('{"type":"subscribe","symbol":"GOOGL"}')
    ws.send('{"type":"subscribe","symbol":"FB"}')
    ws.send('{"type":"subscribe","symbol":"NVDA"}')

    ws.send('{"type":"subscribe","symbol":"JPM"}')
    ws.send('{"type":"subscribe","symbol":"BMW"}')
    ws.send('{"type":"subscribe","symbol":"COKE"}')
    ws.send('{"type":"subscribe","symbol":"TSLA"}')
    ws.send('{"type":"subscribe","symbol":"BERK.A"}')

    ws.send('{"type":"subscribe","symbol":"COINBASE:BTC-USD"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:ETH-USD"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:ADA-USDC"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:BCH-USD"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:EOS-USD"}')

    ws.send('{"type":"subscribe","symbol":"COINBASE:ETC-USD"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:LTC-USD"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:DOGE-USDT"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:SOL-USDT"}')
    ws.send('{"type":"subscribe","symbol":"COINBASE:DASH-USD"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:TRXUSDT"}')

    ws.send('{"type":"subscribe","symbol":"FXCM:XRP/USD"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BNBUSDT"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:VETUSDT"}')
    #ws.send('{"type":"subscribe","symbol":"NEO/USD"}')
    #ws.send('{"type":"subscribe","symbol":"XMR/USD"}')

    ws.send('{"type":"subscribe","symbol":"FXCM:EUR/USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:EUR/NOK"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:AUD/CAD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:GBP/USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:AUD/CHF"}')

    ws.send('{"type":"subscribe","symbol":"FXCM:AUD/USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:EUR/SEK"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:USD/JPY"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:USD/CAD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:AUD/JPY"}')

    ws.send('{"type":"subscribe","symbol":"FXCM:NZD/USD"}')
    ws.send('{"type":"subscribe","symbol":"FXCM:CAD/CHF"}')
    # ws.send('{"type":"subscribe","symbol":"ABNB"}')
    # ws.send('{"type":"subscribe","symbol":"ABNB"}')
    # ws.send('{"type":"subscribe","symbol":"ABNB"}')



def ws_main():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c6qs3gaad3i891nj6ql0",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
