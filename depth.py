import requests
import time
import pyopencl as cl
from pyopencl import array
import numpy as np

def getDepth(symbol1, symbol2, quantity):
    ret = np.empty([quantity*3], cl.array.vec.float4)
    #Binance
    symbol = symbol1+symbol2
    payload={"symbol":symbol, "limit": 100}
    depthDict = requests.get("https://api.binance.com/api/v1/depth", payload).json()
    bidsDict = depthDict["bids"]
    asksDict = depthDict["asks"]
    for i in range(0, quantity):
        tmpvec = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
        ret[i] = tmpvec
    #Bitfinex
    symbol = "t"+symbol1
    if symbol2 == "USDT":
        symbol += "USD"
    else:
        symbol += symbol2
    depthDict = requests.get("https://api.bitfinex.com/v2/book/"+symbol+"/P0"+"?len=100").json()
    bidsDict = depthDict[0:quantity]
    asksDict = depthDict[quantity:]
    for i in range(0,quantity):
        tmpvec = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][2], asksDict[i][0], asksDict[i][2])
        ret[quantity+i] = tmpvec
    #Huobi
    symbol = symbol1+symbol2
    symbol= symbol.lower()
    depthDict = requests.get("https://api.huobipro.com/market/depth?symbol=" + symbol + "&type=step0").json()
    bidsDict = depthDict["tick"]["bids"]
    asksDict = depthDict["tick"]["bids"]
    for i in range(0,quantity):
        tmpvec = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
        ret[2*quantity+i] = tmpvec
    return ret
