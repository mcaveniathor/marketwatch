# marketwatch
---
A Python program which requests current trading data for a given trading pair from the public APIs (as of writing) four cryptocurrency exchanges, processes the data -- taking into account the differences in price between the exchanges -- using OpenCL, aggregates the data and outputs it to the standard output and/or a .csv file.

## Supported Exchanges
1. Binance
2. OKEx
3. Bitfinex
4. Huobi
---
## Usage Instructions
### Install dependecies
Follow the instructions located in the [pipenv documentation](https://docs.pipenv.org/install/), then run 
`pipenv install`
### To run:
`pipenv shell`
`pipenv run marketwatch.py`
