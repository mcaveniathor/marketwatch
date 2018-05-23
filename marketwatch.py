#!/usr/bin/python3
import depth
import opencl

if __name__ == "__main__":
    symbol1 = "BTC"
    symbol2 = "USDT"
    choice = ""
    default = ""
    debug = True
    d = ""

    while not (default == "y" or default == "n"):
        default = input("Default options? y/n\n").lower()
    if default == "n":
        while not (choice == "y" or choice == "n"):
            choice = input("Use symbols BTC/USDT? y/n\n").lower()
        if not (choice == "y"):
            symbol1 = input("Please enter the first symbol.n\n")
            symbol2 = input("Please enter the second symbol.\n")
        while not (d == "y" or d == "n"):
            d = input("Debug? y/n\n").lower()
        if d == "n":
            debug = False
    opencl.run(symbol1, symbol2, debug)


