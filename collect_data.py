from core.Markets import GatherData

tickers = ['^IXIC', '^GSPC', '^DJI']

c = GatherData(tickers)
c.gather_data()