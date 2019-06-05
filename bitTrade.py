from coincheck import market, order, account
from zaifapi import *

import sys

#APIキー認証(各取引所で自分のアカウント情報を入れておく)
zaif_secret = "your access key"
zaif_key = "your secret key"

coincheck_key = order.Order(
    access_key="your access key",
    secret_key="your secret key"
)

"""売り買いする数量を決めておく"""
ORDER_AMOUNT = 0.01

"""zaifの板情報取得"""
zaif = ZaifPublicApi()
zaifP = ZaifTradeApi(zaif_key, zaif_secret)

#トレードしたい通貨
pair = "btc_jpy"

#板情報の取得
zaif_board_data = zaif.depth(pair)
zaif_ask_price= zaif_board_data['asks'][0][0]
zaif_bid_price = zaif_board_data['bids'][0][0]

#print(zaif_board_data)
#print("AskPrice:",zaif_ask_price,"BidPrice:",zaif_bid_price)

"""coincheckの板情報取得"""
m = market.Market()
ticker = m.ticker()

coincheck_ask_price = ticker["ask"]
coincheck_bid_price = ticker["bid"]

#print(coincheck_bid_price, coincheck_ask_price)

"""買値、売値の比較"""
#買値を比較
if (coincheck_bid_price < zaif_bid_price):
    bid_max = zaif_bid_price
    bid_max_code = 'zaif'

if (coincheck_bid_price >= zaif_bid_price):
    bid_max = coincheck_bid_price
    bid_max_code = 'coincheck'

#print(bid_max, bid_max_code)

#売値を比較
if (coincheck_ask_price < zaif_ask_price):
    ask_min = coincheck_bid_price
    ask_min_code = "coincheck"

if (coincheck_ask_price >= zaif_ask_price):
    ask_min = zaif_ask_price
    ask_min_code = "zaif"

#print(ask_min, ask_min_code)


"""トレード"""

#買値maxが売値のminより小さい場合にはトレードしない
if(bid_max < ask_min):
    print("買値が売値より小さくなっています")
    sys.exit()

#売値が安い方で買い、買値が高い方で売る
#coincheckの売値が安い場合(coincheckで買い、zaifで売り)
if(ask_min_code == "coincheck"):
    #coincheckで買う
    coincheckResult = coincheck_key.buy_btc_jpy(rate=ask_min, amount=ORDER_AMOUNT)
    print(coincheckResult)
    #zaifで売る
    status = zaifP.trade(currency_pair="btc_jpy", action="ask", price=bid_max, amount=ORDER_AMOUNT)
    print(status)

#zaifの売値が安い場合(zaifで買い、coincheckで売り)
if(ask_min_code == "zaif"):
    #zaifで買う
    zaifResult = zaifP.trade(currency_pair="btc_jpy", action="bid", price=ask_min, amount=ORDER_AMOUNT)
    print(zaifResult)
    #coincheckで売る
    orderPrice = coincheck_bid_price
    coincheckResult = coincheck_key.sell_btc_jpy(rate=bid_max, amount=ORDER_AMOUNT)
    print(coincheckResult)