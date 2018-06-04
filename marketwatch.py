#!/usr/bin/python3
import depth
import opencl
import asyncio
import uvloop
import aiofiles
import ujson
import os.path

async def writeOptions(opt):
    async with aiofiles.open("settings.txt", "w") as f:
        await f.write(ujson.dumps(opt) + "\n")
        await f.close()

async def getOptions():
    opt = {"symbol1": "", "symbol2":"","quantity":0,"iterations":0,"delay":0.0}
    choice = ""
    while not (choice == "y" or choice == "n"):
        choice = input("Use symbols BTC/USDT? y/n\r\n").lower()
        if choice == "y":
            opt["symbol1"] = "BTC"
            opt["symbol2"] = "USDT"
        else:
            opt["symbol1"] = input("Please enter the first symbol.\r\n")
            print("\033[2J\f")
            opt["symbol2"] = input("Please enter the second symbol.\r\n")
    print("\033[2J\f")
    while opt["quantity"] == 0:
        opt["quantity"] = int(input("How many entries from each exchange? Max: 100\r\n"))
    print("\033[2J\f")
    while opt["iterations"] == 0:
        opt["iterations"] = int(input("How many iterations would you like to run? -1 to run forever\r\n"))
    print("\033[2J\f")
    while opt["delay"] == 0.0:
        opt["delay"] = float(input("How many seconds would you like to sleep between each iteration?\r\n"))
    print("\033[2J\f")
    return opt

async def first_run():
    print("Welcome to marketwatch!\r\nWe will now set up marketwatch with the default settings of your choosing.\r\n")
    opt = await getOptions()
    await writeOptions(opt)

async def main():
    opt = {"symbol1": "", "symbol2":"","quantity":0,"iterations":0,"delay":0.0}
    if not os.path.isfile("./settings.txt"):
        await first_run()
    async with aiofiles.open("settings.txt", "r") as f:
        opt = ujson.loads(await f.read())
        await f.close()
    default = ""
    while not (default == "y" or default == "n"):
        default = input("Default options? y/n\r\n").lower()
    if default == "n":
        opt = await getOptions()
    print("\033[2J\f")
    await opencl.run(opt["symbol1"], opt["symbol2"], opt["quantity"], opt["iterations"], opt["delay"])

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
