# marketwatch
Install dependencies:
`pip install docopt`
---
## Exchanges
1. Binance
2. OKEx
3. Bitfinex
4. Huobi
---
## Usage Instructions
To clear csv file (leaving the header):
`python3 marketwatch.py clear`

To run:
`python3 marketwatch.py watch [--print] [--filename=<filename>] [--exchange=<exchange>] <symbol> [<symbol>] [--time=<time>]`

For example, to pull BTC/USD data from Binance for 20 seconds, print it to console and to depth.csv:
`python3 marketwatch.py watch --print --filename depth.csv --exchange 1 BTC --symbol2 USDT --time 20`

Or, making use of the default values for command line arguments:
`python3 marketwatch.py` watch --print BTC --time 20

Set the time flag to -1 to run indefinitely:
`python3 marketwatch.py watch BTC -1`

To see all command line options:
`python3 marketwatch.py -h`

