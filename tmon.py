import logging
import curses
import time
import os
import json

""" move this to a config file later.. """
from binance.client import Client
from binance.depthcache import DepthCacheManager

""" Configure prod vs dev modes """
testnet = False
mainnet = True

global asks
global bids

try:
    if mainnet:
        client = Client("API_TOKEN", "SECRET_KEY")
    if testnet:
        client = Client("API_TOKEN", "SECRET_KEY")
        client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
except Exception as e:
    print(e)


screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)


def percent(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    percentage = '{0:.2f}'.format((num1 / num2 * 100))
    return percentage

def process_depth(depth_cache):
    if depth_cache is not None:
        ask_count = len(depth_cache.get_asks())
        bid_count = len(depth_cache.get_bids())
        total = ask_count + bid_count
        if float(percent(bid_count, total)) > 50:
            pair = 2
        else:
            pair = 1
        screen.addstr("LONG: {}% SHORT: {}%".format(percent(bid_count, total), percent(ask_count, total)), curses.color_pair(pair))
        screen.refresh()
        screen.clear()

dcm = DepthCacheManager(client, 'BTCUSDT', callback=process_depth, refresh_interval=0)
