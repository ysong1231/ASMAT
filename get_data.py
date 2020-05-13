from core.Markets import HistoricalData

h = HistoricalData()

for ticker in ['^IXIC', '^DJI', '^GSPC', '^VIX']:
    h.pull_historical_data(ticker, '2000-1-1', '2020-5-30')