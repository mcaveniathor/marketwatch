import requests
import time
import threading
import csv
import numpy as np
import pyopencl as cl

def getDepth(exchange, quantity, symbol1, symbol2, debug):
    ret = np.empty([quantity], cl.array.vec.float4)
    if exchange == "binance":
        #Binance
        symbol = symbol1+symbol2
        payload={"symbol":symbol, "limit":"20"}
        depthDict = requests.get("https://api.binance.com/api/v1/depth", payload).json()
        bidsDict = depthDict["bids"]
        asksDict = depthDict["asks"]
        for i in range(0, quantity):
            tmpvec = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
            ret[i] = tmpvec
    #Bitfinex
    if exchange == "bitfinex":
        if symbol2 == "USDT":
            symbol2 = "USD"
        symbol = symbol1+symbol2
        depthDict = requests.get("https://api.bitfinex.com/v1/book/"+symbol).json()
        if symbol1 == "USD":
            symbol1 = "USDT"
        if symbol2 == "USD":
            symbol2 = "USDT"
        bidsDict = depthDict["bids"]
        asksDict = depthDict["asks"]
        for i in range(0,20):
            tmpvec = cl.array.vec.make_float4(bidsDict[i]["price"], bidsDict[i]["amount"], asksDict[i]["price"], asksDict[i]["amount"])
            ret[i] = tmpvec
    #Huobi
    if exchange == "huobi":
        symbol = symbol1+symbol2
        depthDict = requests.get("https://api.huobipro.com/market/depth", {"symbol": symbol.lower(), "type": "step0"}).json()
        bidsDict = depthDict["tick"]["bids"]
        asksDict = depthDict["tick"]["asks"]
        for i in range(0,20):
            tmpvec = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
            ret[i] = tmpvec
    return ret
