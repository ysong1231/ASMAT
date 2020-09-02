from core.Markets import StockData
from datetime import datetime, timedelta

now = datetime.now()
start = (now - timedelta(days = now.weekday())).strftime('%Y-%m-%d')
end = now.strftime('%Y-%m-%d')

tickers = [
    '^IXIC', 
    '^DJI', 
    '^GSPC', 
    '^RUT', 
    '^VIX', 
    'AAPL', 
    'FB', 
    'GOOG', 
    'ZM', 
    'TSLA', 
    'MSFT', 
    'AMZN'
] 

sd = StockData(start = start, end = end, tickers = tickers)
sd.collect()

time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
end = (now - timedelta(days = 1)).strftime('%Y-%m-%d')
print(f'[{time}] {start} - {end} Intraday Data Entered into Database!')