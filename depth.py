import requests
import time
import threading
import csv
import numpy as np
import pyopencl as cl

def getDepth(symbol1, symbol2, debug):
    ret = np.empty((2, 3, 20, 2))
    bids = np.empty((3, 20, 2))
    asks = np.empty((3, 20, 2))
    #Binance
    symbol = symbol1+symbol2
    payload={"symbol":symbol, "limit":"20"}
    depthDict = requests.get("https://api.binance.com/api/v1/depth", payload).json()
    tmp = depthDict["bids"]
    for i in range(0, 20):
        bids[0,i] = tmp[i][0:2]
        if debug:
            print("bids[0,"+str(i)+"]")
            print(bids[0,i])
    tmp = depthDict["asks"]
    for i in range(0,20):
        asks[0,i] = tmp[i][0:2]
        if debug:
            print("asks[0,"+str(i)+"]")
            print(asks[0,i])
    #Bitfinex
    if symbol2 == "USDT":
        symbol2 = "USD"
    symbol = symbol1+symbol2
    depthDict = requests.get("https://api.bitfinex.com/v1/book/"+symbol).json()
    if symbol1 == "USD":
        symbol1 = "USDT"
    if symbol2 == "USD":
        symbol2 = "USDT"
    tmp = depthDict["bids"]
    for i in range(0,20):
        bids[1,i] = ([tmp[i]["price"], tmp[i]["amount"]])
        if debug:
            print("bids[1,"+str(i)+"]")
            print(bids[1,i])
    tmp = depthDict["asks"]
    for i in range(0,20):
        asks[1,i] = ([tmp[i]["price"], tmp[i]["amount"]])
        if debug:
            print("asks[1,"+str(i)+"]")
            print(asks[1,i])
    #Huobi
    symbol = symbol1+symbol2
    depthDict = requests.get("https://api.huobipro.com/market/depth", {"symbol": symbol.lower(), "type": "step0"}).json()
    tmp = depthDict["tick"]["bids"]
    for i in range(0,20):
        bids[2,i] = tmp[i]
        if debug:
            print("bids[2," + str(i) + "]")
            print(bids[2,i])
    tmp = depthDict["tick"]["asks"]
    for i in range(0,20):
        asks[2,i] = tmp[i]
        if debug:
            print("asks[3," + str(i) + "]")
            print(asks[2,i])
    ret[0] = bids
    ret[1] = asks
    return ret
