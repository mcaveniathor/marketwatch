import requests
import time
import threading
import csv

#by default, assume USDT as the second symbol
#TODO: log depth beyond high bid and low ask
def getDepth(exchange, symbol1, symbol2="USDT"):
    highestBid = 0.0
    lowestAsk = 0.0
    tickerPrice = 0.0
    #Binance
    if exchange == 1:
        symbol = symbol1+symbol2
        payload={"symbol":symbol, "limit":"5"}
        depthDict = requests.get("https://api.binance.com/api/v1/depth", payload).json()
        #tickerDict= requests.get("https://api.binance.com/api/v3/ticker/price", {"symbol": symbol}).json()
        #tickerPrice = float(tickerDict["price"])
        highestBid = float(depthDict["bids"][0][0])
        lowestAsk = float(depthDict["asks"][0][0])
    #Either I'm an idiot or it is actually this simple(?)
    computedPrice = (((highestBid) + (lowestAsk)) / 2.0)
    highestBidPercent = (highestBid / computedPrice * 100.0)
    lowestAskPercent = (lowestAsk / computedPrice * 100.0)
    bidAskSpread = ((lowestAskPercent - highestBidPercent) / lowestAskPercent)
    #Probably useless information, but collected it anyway
    #print("Ticker Price: " + str(tickerPrice))
    #print("Ticker Price % Error: " + str(((computedPrice - tickerPrice) / computedPrice) * 100))
    #print("Computed Price: " + str(computedPrice))
    #print("Highest bid: " + str(highestBid))
    #print("Lowest ask: " + str(lowestAsk))
    #print("Highest bid as a percentage of computed price : " + str(highestBidPercent))
    #print("Lowest ask as a percentage of computed price : " + str(lowestAskPercent))
    return({"exchange": exchange, "symbol": symbol, "price": computedPrice, "highestBidPercent": highestBidPercent, "lowestAskPercent": lowestAskPercent, "bidAskSpread": bidAskSpread, "time": time.time()})

def writeDepth(filename, exchange, symbol1, symbol2, iterations):
    with open(filename, "a") as depthCSV:
        fieldNames = ["exchange", "symbol", "price", "highestBidPercent", "lowestAskPercent", "bidAskSpread", "time"]
        depthWriter = csv.DictWriter(depthCSV, fieldnames = fieldNames)
        if iterations == -1:
            while True:
                depthWriter.writerow(getDepth(exchange, symbol1, symbol2))
                time.sleep(.1)
        else:
            for i in range(0, iterations):
                depthWriter.writerow(getDepth(exchange, symbol1, symbol2))
                time.sleep(.1)

