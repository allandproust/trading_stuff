"""

Monitors BTC price across 9 exchanges, returns an average.

"""


import os
import sys
import time
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402


def print_exchanges():
    dump('Supported exchanges:', ', '.join(ccxt.exchanges))


def print_ticker(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol.upper())
    dump(
        exchange,
        'ask: ' + str(ticker['ask']))

while True:
    try:
        agg_prices = []
        exchanges = ['binance', 'coinbasepro', 'bybit', 'kraken', 'bitmex',  'okcoin', 'binanceus', 'gemini', 'bitstamp']
        for id in exchanges:
            exchange_found = id in ccxt.exchanges

            # instantiate the exchange by id
            exchange = getattr(ccxt, id)()
            symbol = "BTC/USD"

            try:
                if id == "binance":
                    symbol = "BTC/USDT"
                if id == "coinbasepro":
                    symbol = "BTC/USD"
                if id == "bybit":
                    symbol = "BTC/USD"
                if id == "kraken":
                    symbol = "BTC/USD"
                
                #print_ticker(exchange, symbol)
                ask_price = exchange.fetch_ticker(symbol.upper())['ask'] 
                agg_prices.append(ask_price)
               
            except ccxt.DDoSProtection as e:
                print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
            except ccxt.RequestTimeout as e:
                print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
            except ccxt.ExchangeNotAvailable as e:
                print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
            except ccxt.AuthenticationError as e:
                print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')


    except Exception as e:

        print(type(e).__name__, e.args, str(e))

    #print(agg_prices) 
    print("Average: {}".format(round(sum(agg_prices) / len(agg_prices),2)))
