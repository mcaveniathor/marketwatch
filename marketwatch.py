#!/usr/bin/python3
import depth
import opencl
import asyncio
import uvloop

async def main():
    symbol1 = "BTC"
    symbol2 = "USDT"
    choice = ""
    default = ""
    quantity = 0
    iterations = 0
    delay = 0.0
    while not (default == "y" or default == "n"):
        default = input("Default options? y/n\r\n").lower()
    if default == "n":
        print("\033[2J\f")
        while not (choice == "y" or choice == "n"):
            choice = input("Use symbols BTC/USDT? y/n\r\n").lower()
        if not (choice == "y"):
            symbol1 = input("Please enter the first symbol.\r\n")
            print("\033[2J\f")
            symbol2 = input("Please enter the second symbol.\r\n")
        print("\033[2J\f")
        while quantity == 0:
            quantity = int(input("How many entries from each exchange? Max: 100\r\n"))
        print("\033[2J\f")
        while iterations == 0:
            iterations = int(input("How many iterations would you like to run? -1 to run forever\r\n"))
        print("\033[2J\f")
        while delay == 0.0:
            delay = float(input("How many seconds would you like to sleep between each iteration?\r\n"))
    else:
        symbol1 = "BTC"
        symbol2 = "USDT"
        quantity = 100
        iterations = -1
        delay = 1.0
    print("\033[2J\f")
    await opencl.run(symbol1, symbol2, quantity, iterations, delay)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
