import asyncio
import aiohttp
import pyopencl as cl
import ujson as json
from pyopencl import array
import numpy as np

async def binanceDepth(symbol1, symbol2, quantity, session):
    ret = np.empty([quantity], cl.array.vec.float4)
    params = {"symbol": symbol1+symbol2, "limit":100}
    async with session.get("https://api.binance.com/api/v1/depth", params=params) as resp:
        depthDict = await resp.json()
        bidsDict = depthDict["bids"]
        asksDict = depthDict["asks"]
        for i in range(0,quantity):
            ret[i] = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
        return ret

async def bitfinexDepth(symbol1, symbol2, quantity, session):
    ret = np.empty([quantity], cl.array.vec.float4)
    symbol = "t"+symbol1
    if symbol2 == "USDT":
        symbol += "USD"
    params = {"len": 100}
    async with session.get("https://api.bitfinex.com/v2/book/" + symbol + "/P0", params=params) as resp:
        depthDict = await resp.json()
        bidsDict = depthDict[0:quantity]
        asksDict = depthDict[quantity:]
        for i in range(0,quantity):
            ret[i] = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][2], asksDict[i][0], asksDict[i][2])
        return ret

async def huobiDepth(symbol1, symbol2, quantity, session):
    ret = np.empty([quantity], cl.array.vec.float4)
    params = {"symbol": (symbol1+symbol2).lower(), "type": "step0"}
    async with session.get("https://api.huobi.pro/market/depth?symbol=btcusdt&type=step0")as resp:
        depthDict = await resp.json(content_type=None)
        bidsDict = depthDict["tick"]["bids"]
        asksDict = depthDict["tick"]["asks"]
        for i in range(0, quantity):
            ret[i] = cl.array.vec.make_float4(bidsDict[i][0], bidsDict[i][1], asksDict[i][0], asksDict[i][1])
        return ret

async def getDepth(symbol1, symbol2, quantity):
    async with aiohttp.ClientSession() as session:
        tasks = [binanceDepth(symbol1, symbol2, quantity, session), bitfinexDepth(symbol1, symbol2, quantity, session), huobiDepth(symbol1, symbol2, quantity, session)]
        done, pending = await asyncio.wait(tasks)
        ret = np.empty([0,], cl.array.vec.float4)
        prices = np.empty([3,], float)
        for i in range(0, len(done)):
            tmp = done.pop().result()
            ret = np.append(ret, tmp)
            prices[i] = (tmp[0][0]+tmp[0][2])/2.0
        return ret, prices

