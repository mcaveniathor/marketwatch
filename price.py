import requests
import csv
import time
import threading
filename = "binance_price.csv"

class priceThread(threading.Thread):
    def __init__(self, symbol, threadID):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.threadID = threadID


def getPrice(sym):
        payload={"symbol":sym}
        priceDict= requests.get("https://api.binance.com/api/v3/ticker/price", payload).json()
        priceDict["time"] = time.time()
        return priceDict
def write(sym, delay):
    with open("price.csv", "a") as csvfile:
        fieldnames = ["symbol", "price", "time"]
        priceWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        while True:
           priceDict = getPrice(sym)
           priceWriter.writerow(priceDict)
           time.sleep(delay)
symbols = ["BTCUSDT", "ETHUSDT"]
class ThreadPool():
    threads = []
    def __init__(self, symbols):
        counter = 0
        for symbol in symbols:
            threads.append(PriceThread(i, counter))
            threads[counter].start()
            counter += 1
    def joinThreads()
        for thread in threads:
            thread.join()



