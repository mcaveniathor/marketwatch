#!/usr/bin/python3
"""marketwatch
Usage:
    marketwatch.py watch [--print] [--filename=<filename>] [--exchange=<exchange>] <symbol1> [--symbol2=<symbol2>] [--time=<time>]
    marketwatch.py clear [<filename>]
    marketwatch.py -h | --help
Options:
    --print                 print data to standard output [default: True]
    --filename=<filename>   output csv data to specified file [default: depth.csv]
    --exchange=<exchange>   pull data from specified exchange [default: 1]
    --symbol2=<symbol2>     specify the second symbol [default: USDT]
    --time=<time>           run for a specified time in seconds or set to -1 to run indefinitely [default: -1]
    -h --help               show this screen
"""

from docopt import docopt
import depth
import time

if __name__ == "__main__":
    arguments = docopt(__doc__, version="marketwatch 0.1")

if arguments["watch"]:
    depth.spawnThreads(arguments["--filename"], int(arguments["--exchange"]), arguments["<symbol1>"], arguments["--symbol2"], float(arguments["--time"]), arguments["--print"])

if arguments["clear"]:
    f = open(arguments["--filename"], "w")
    f.write("exchange, symbol, price, highestBidPercent, highestAskPercent, bidAskSpread, time\n")
    f.close()
