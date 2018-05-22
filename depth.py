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
        if symbol1 == "USDT":
            symbol1 = "USD"
        if symbol2 == "USDT":
            symbol2 = "USD"
        symbol = symbol1+symbol2
        depthDict = requests.get(("https://api.bitfinex.com/v1/book/"+symbol)).json()
        highestBid = float(depthDict["bids"][0]["price"])
        lowestAsk = float(depthDict["asks"][0]["price"])
    #Huobi
    if exchange == 4:
        symbol = symbol1+symbol2
        depthDict = requests.get("https://api.huobipro.com/market/depth", {"symbol": symbol.lower(), "type": "step0"}).json()
        highestBid = float(depthDict["tick"]["bids"][0][0])
        lowestAsk = float(depthDict["tick"]["asks"][0][0])

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
            "highestBidPercent": highestBidPercent, "lowestAskPercent": lowestAskPercent, 
            "bidAskSpread": bidAskSpread, "time": time.time()})


#each scraperThread pulls and writes data for  given exchange concurrently
threadLock = threading.Lock()
class scraperThread(threading.Thread):
    def __init__(self, filename, exchange, symbol1, symbol2, t, log):
        threading.Thread.__init__(self)
        self.filename = filename
        self.exchange = exchange
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.t = t
        self.log = log
    def run(self):
        threadLock.acquire()
        writeDepth(self.filename, self.exchange, self.symbol1, self.symbol2, self.t, self.log)
        threadLock.release()

#Create an array of scraperThreads -- one for each exchange
def spawnThreads(filename, exchanges, symbol1, symbol2, t, log):
    threads = []
    for exchange in exchanges:
        thread = scraperThread(filename, exchanges, symbol1, symbol2, t, log)
        threads.append(thread)
        thread.start()

#used to timeout the writeDepth function when it is passed a t parameter which is not -1
endFlag = False
timeLock = threading.Lock()
class endThread(threading.Thread):
    def __init__(self, t):
        threading.Thread.__init__(self)
        self.t = t
    def run(self):
        global endFlag
        timeLock.acquire()
        time.sleep(self.t)
        endFlag = True
        timeLock.release()

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
