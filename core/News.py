import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
    
class WebpageNews:
    def __init__(self):
        self.url = 'https://finance.yahoo.com/topic/stock-market-news'
        datetime.now().strftime('%Y%m%d')
        
    def _get_response(self):
        rsp = requests.get(self.url)
        self.rsp = rsp
    
    def _parse_news_items(self):
        soup = BeautifulSoup(self.rsp.text, 'html.parser')
        news_containers = soup.find_all('div', class_ = 'Py(14px) Pos(r)')
        news_items = []
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M')
        for news in news_containers:
            item = {}
            item['title'] = news.find('a').text
            item['description'] = news.find('p').text
            item['href'] = 'https://finance.yahoo.com' + news.find('a')['href']
            item['source'] = news.find('div', class_ = 'C(#959595) Fz(11px) D(ib) Mb(6px)').text
            item['date'] = date
            item['time'] = time
            news_items.append(item)
        self.df = pd.DataFrame(news_items)
    
    def _to_database(self):
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/stock')
        c = 0
        for i in range(len(self.df)):
            try:
                self.df.iloc[i:i+1].to_sql('news', con = engine, index = False, if_exists = 'append')
                c += 1
            except:
                pass
        return c

    def collect(self):
        self._get_response()
        self._parse_news_items()
        return self._to_database()
        


