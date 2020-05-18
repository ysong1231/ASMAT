import datetime
from core.Markets import HistoricalData

h = HistoricalData()

for ticker in ['^IXIC', '^DJI', '^GSPC', '^VIX']:
    h.pull_historical_data(
        ticker,
        (datetime.date.today() + datetime.timedelta(-3*30)).strftime("%Y-%m-%d"),
        datetime.date.today().strftime("%Y-%m-%d"),
        save_path = "prediction_data"
    )