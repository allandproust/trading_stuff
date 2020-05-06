import logging
import time
import dataset
import psycopg2
import pickle
import os

import json
import requests

""" move this to a config file later.. """
from binance.client import Client
from binance.websockets import BinanceSocketManager

"""
{u'E': 1588304329273,
 u'M': True,
 u'T': 1588304329272,
 u'a': 281003382,
 u'e': u'aggTrade',
 u'f': 306070636,
 u'l': 306070636,
 u'm': False,
 u'p': u'8703.01000000',
 u'q': u'2.00000000',
 u's': u'BTCUSDT'}
"""

"""
SELECT COUNT(data->>'q') as quantity, CAST (data->>'p' AS FLOAT) as cost, data->>'a' as SellerOrderID from "TRADING".trades
GROUP BY  SellerOrderID , cost
ORDER BY quantity DESC
"""
pgconn = psycopg2.connect(user="???????????",
			      password="??????????",
			      host="127.0.0.1",
			      port="5432",
			      database="trading")

while True:
    webhook_url= 'https://hooks.slack.com/services/?????????????????????????????????????????????????'
    find_whales_query = """ SELECT quantity, cost, SellerOrderID from (SELECT COUNT(data->>'q') as quantity, CAST (data->>'p' AS FLOAT) as cost, data->>'a' as SellerOrderID from "TRADING".trades
                            GROUP BY  SellerOrderID , cost) t
                            WHERE quantity > 100
                            ORDER BY quantity DESC"""
    cursor = pgconn.cursor()
    cursor.execute(find_whales_query)
    prev_whale_trades = ()
    if os.path.exists("whales.p"):
        print("loading old whale data... pls hold")
        prev_whale_trades = pickle.load(open("whales.p", "rb"))
        print("{} historical whales loaded.".format(len(prev_whale_trades)))
    whale_trades = cursor.fetchall()
    print("Getting new data from Postgres..")
    pickle.dump(whale_trades, open( "whales.p", "wb" ) )
    print("Saved new data to pickle.")
 
    for trade in whale_trades:
        print("Processing new data..")
        if trade not in prev_whale_trades:
            msg = "Detected WHALE trade: {} BTC sold to USDT on Binance Futures @ {} - total cost: ${} USDT".format(trade[0], trade[1],(trade[0] * trade[1]))
            print(msg)
            slack_data = {'text': msg}
            response = requests.post(
                webhook_url, data=json.dumps(slack_data),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code != 200:
                raise ValueError(
                    'Request to slack returned an error %s, the response is:\n%s'
                     % (response.status_code, response.text))
        print("Sleeping for 5.")
        time.sleep(5)



 
