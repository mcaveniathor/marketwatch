import requests
import time
import threading
import csv

#TODO: log depth beyond high bid and low ask
def getDepth(exchange, symbol1, symbol2):
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

    #Bitfinex
    if exchange == 3:
        if symbol2 == "USDT":
            symbol2 = "USD"
        symbol = symbol1+symbol2
        depthDict = requests.get(("https://api.bitfinex.com/v1/book/"+symbol)).json()
        highestBid = float(depthDict["bids"][0]["price"])
        lowestAsk = float(depthDict["asks"][0]["price"])

    computedPrice = (((highestBid) + (lowestAsk)) / 2.0)
    #Compute the highest bid and lowest ask as a percentage of the calculated price for the given exchange
    #this normalizes the data, allowing for apples-to-apples comparison between exchanges
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
    return({"exchange": exchange, "symbol": symbol, "price": computedPrice,
            "highestBidPercent": highestBidPercent, "lowestAskPercent": lowestAskPercent, "bidAskSpread": bidAskSpread, "time": time.time()})


endFlag = False
threadLock = threading.Lock()
class endThread(threading.Thread):
    def __init__(self, t):
        threading.Thread.__init__(self)
        self.t = t
    def run(self):
        global endFlag
        threadLock.acquire()
        time.sleep(self.t)
        endFlag = True
        threadLock.release()

def writeDepth(filename, exchange, symbol1, symbol2, t, log):
    with open(filename, "a") as depthCSV:
        fieldNames = ["exchange", "symbol", "price", "highestBidPercent", "lowestAskPercent", "bidAskSpread", "time"]
        depthWriter = csv.DictWriter(depthCSV, fieldnames = fieldNames)
        if t == -1:
            while True:
                row = getDepth(exchange, symbol1, symbol2)
                depthWriter.writerow(row)
                if log:
                    print(row)
                time.sleep(.1)
        else:
            end = endThread(t)
            end.start()
            while not endFlag:
                row = getDepth(exchange, symbol1, symbol2)
                depthWriter.writerow(row)
                if log:
                    print(row)
                time.sleep(.1)
