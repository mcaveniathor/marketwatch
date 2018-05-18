#!/usr/bin/python3
# 0 - OKEx
# 1 - Binance
# 2 - Bitfinex
# 3 - Huobi
import depth

#last parameter is number of iterations. set to -1 for infinite loop
depth.writeDepth("depth.csv", 1, "BTC", "USDT", 10)


#WIP
'''
import queue
import threading

exitFlag = False
class WorkerThread(threading.Thread):
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q

def run(threadID, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            job = workQueue.get()
            print("Starting thread " + str(threadID) + "with job " + job)
            if job == "depth":
                depth.writeDepth("depth.csv")
        queLock.release()

numThreads = 1
queueLock = threading.Lock()
workQueue = queue.Queue(numThreads)
threads = []
for i in range(0, numThreads):
    thread = WorkerThread(i, workQueue)
    thread.start()
    threads.append(thread)

queueLock.acquire()
workQueue.put("depth")
queueLock.release()
while not workQueue.empty():
    pass
exitFlag = 1
for thread in threads:
    thread.join()
'''
