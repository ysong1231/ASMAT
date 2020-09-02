import os
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

class StockData():
    def __init__(self, start = None, end = None, interval = '1m', tickers = None):
        self.start = start
        self.end = end
        self.interval = interval
        self.tickers = tickers

    def _yfinance_collector(self):
        data = yf.download(
            tickers = ' '.join(self.tickers),
            start = self.start,
            end = self.end,
            interval = self.interval,
            group_by = 'ticker',
            threads = True
        )
        self.data = data

    def _format_data(self):
        df = pd.DataFrame()
        for t in self.tickers:
            self.data[(t, 'ticker')] = t
            df = pd.concat([df, self.data[t]])
        df = df.reset_index()
        df['date'] = df['Datetime'].apply(lambda x: x.date())
        df['time'] = df['Datetime'].apply(lambda x: x.time())
        df = df.drop(['Datetime'], axis = 1).rename(columns = {'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace = False)
        self.df = df

    def _to_database(self):
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/stock')
        self.df.to_sql(
            'intraday', 
            con = engine,
            index = False,
            if_exists = 'append'
        )
        
    def collect(self):
        self._yfinance_collector()
        self._format_data()
        self._to_database()
