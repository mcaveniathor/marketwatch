import asyncio
import aiohttp
import pyopencl as cl
from pyopencl import array
import numpy as np
import hashlib

async def binanceDepth(symbol1, symbol2, quantity, session):
    ret = np.empty([quantity], cl.array.vec.float4)
    if quantity > 50:
        limit = 100
    elif quantity > 20:
        limit = 50
    elif quantity > 10:
        limit = 20
    elif quantity > 5:
        limit = 10
    else:
        limit = 5
    params = {"symbol": symbol1+symbol2, "limit":limit}
    async with session.get("https://api.binance.com/api/v1/depth", params=params) as resp:
        depthDict = await resp.json()
        bidsDict = depthDict["bids"]
        asksDict = depthDict["asks"]
        for i in range(0,quantity):
            ret[i] = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
        return ret, "Binance"

async def bitfinexDepth(symbol1, symbol2, quantity, session):
    ret = np.empty([quantity], cl.array.vec.float4)
    if quantity > 25:
        limit = 100
    else:
        limit = 25
    symbol = "t"+symbol1
    if symbol2 == "USDT":
        symbol += "USD"
    params = {"len": limit}
    async with session.get("https://api.bitfinex.com/v2/book/" + symbol + "/P0", params=params) as resp:
        depthDict = await resp.json()
        bidsDict = depthDict[0:quantity]
        asksDict = depthDict[quantity:]
        for i in range(0,quantity):
            ret[i] = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][2], asksDict[i][0], asksDict[i][2])
        return ret, "Bitfinex"

async def huobiDepth(symbol1, symbol2, quantity, session):
    ret = np.empty([quantity], cl.array.vec.float4)
    if quantity > 20:
        limit = "step0"
    else:
        limit = "step1"
    params = {"symbol": (symbol1+symbol2).lower(), "type": limit}
    async with session.get("https://api.huobi.pro/market/depth", params=params)as resp:
        depthDict = await resp.json(content_type=None) #Huobi's API gives data as the wrong datatype, 
        bidsDict = depthDict["tick"]["bids"]           #so disable type checking
        asksDict = depthDict["tick"]["asks"]
        for i in range(0, quantity):
            ret[i] = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
        return ret, "Huobi"

async def okexDepth(symbol1, symbol2, quantity, session, apiKeys):
    ret = np.empty([quantity], cl.array.vec.float4)
    if symbol2 == "USDT":
        symbol2 = "usd"
    p = "?api_key="+apiKeys[0]+"&size="+str(quantity)+"&symbol="+(symbol1+"_"+symbol2).lower()+"&secret_key="+apiKeys[1]
    m = hashlib.md5()
    m.update(p.encode())
    params = {"sign":m.digest().upper()}
    async with session.get("https://www.okex.com/api/v1/depth.do", params=params) as resp:
        depthDict = await resp.json()
        print(depthDict)
        bidsDict = depthDict["bids"]
        asksDict = depthDict["asks"]
        for i in range(0, quantity):
            ret[i] = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
        return ret, "OKEx"

async def calcPrice(arr, quantity):
    numEx = (arr.size/quantity)
    p = np.zeros([numEx,])
    for i in range(0, numEx):
        p[i] = float(arr[0] + arr[2])/2.0
    return cl.array.vec.make_float4(p[0],p[1],p[2],p[3])

async def getDepth(symbol1, symbol2, quantity):
    async with aiohttp.ClientSession() as session:
        tasks = [binanceDepth(symbol1, symbol2, quantity, session), bitfinexDepth(symbol1, symbol2, quantity, session), huobiDepth(symbol1, symbol2, quantity, session)] #okexDepth(symbol1, symbol2, quantity, session, apiKeys)
        done, pending = await asyncio.wait(tasks)
        ret = np.empty([0,], cl.array.vec.float4)
        exchanges = []
        for i in range(0, len(done)):
            tmp = done.pop().result()
            ret = np.append(ret, tmp[0])
            exchanges.append(tmp[1])
        prices = await calcPrice(ret, quantity)
        return ret, prices, exchanges

