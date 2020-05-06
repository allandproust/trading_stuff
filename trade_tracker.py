import time
import dataset
import psycopg2

""" move this to a config file later.. """
from binance.client import Client
from binance.websockets import BinanceSocketManager

""" Configure prod vs dev modes """
testnet = False
mainnet = True

try:
    if mainnet:
        client = Client("API_TOKEN", "SECRET_KEY")
    if testnet:
        client = Client("API_TOKEN", "SECRET_KEY")
        client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
except Exception as e:
    print(e)


def construct_pg_url(postgres_user='?????????', postgres_password='????????????', postgres_host='localhost', postgres_port='5432', postgres_database='trading'):
    PG_URL = "postgresql://" + postgres_user + ":" + postgres_password + '@' + postgres_host + ':' + postgres_port + '/' + postgres_database
    return PG_URL


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

pgconn = dataset.Database(
	     url=construct_pg_url(),
	     schema='TRADING'
)
def process_message(msg):
    table = pgconn['trades']
    row = dict(data=msg)
    table.insert(row)
    print(msg)

 
bm = BinanceSocketManager(client)
conn_key = bm.start_trade_socket('BTCUSDT', process_message)
bm.start()
