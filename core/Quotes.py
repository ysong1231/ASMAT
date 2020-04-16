import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from common_tools.send_email import send_email

load_dotenv()

class Quotes:
    def __init__(self, market_index):
        if market_index == 'S&P500':
            self.url = 'https://financialmodelingprep.com/api/v3/quote/%5EGSPC'
        elif market_index == 'DOW':
            self.url = 'https://financialmodelingprep.com/api/v3/quote/%5EDJI'
        elif market_index == 'NASDAQ':
            self.url = 'https://financialmodelingprep.com/api/v3/quote/%5EIXIC'
        else:
            raise ValueError('Invalid market index name!')

        if os.getenv('VERSION') == 'local':
            self.conf_path = 'conf/.quotes.json'
        if os.getenv('VERSION') == 'production':
            self.conf_path = '/home/ec2-user/ASMAT/conf/.quotes.json'

        self.mkt = market_index
        self.FLOAT_THRESHOLD = 0.005

    def get_quote(self):
        with requests.Session() as s:
            request = s.get(self.url, timeout=15)
            quote_data = request.json()[0]
        return quote_data
    
    def load_last_quote(self):
        with open(self.conf_path) as json_file:
            last_quote = json.load(json_file)
        return last_quote
    
    def record_quote(self, q):
        with open(self.conf_path, 'w') as json_file:
            json.dump(q, json_file)
    
    def ts_to_date(self, ts):
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

    def real_time_check(self):
        new_quote = self.get_quote()
        old_quote = self.load_last_quote()
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if self.ts_to_date(new_quote.get('timestamp')) != self.ts_to_date(old_quote.get('timestamp')):
            new_quote['dayOpen'] = new_quote['open']
            self.record_quote(new_quote)
            print(f'[{time}] First quote of the day')
            return

        float_rate = (new_quote.get('price') - old_quote.get('price')) / old_quote.get('dayOpen')
        
        if float_rate >= self.FLOAT_THRESHOLD:
            send_email(
                f'Subject: {self.mkt} Up {round(float_rate * 100, 2)}%\n\n{new_quote}'
            )
            new_quote['dayOpen'] = old_quote['dayOpen']
            self.record_quote(new_quote)
            print(f'[{time}] {self.mkt} Up {round(float_rate * 100, 2)}% | Alerting email sent | New quote recorded')
            return
        
        if float_rate <= -self.FLOAT_THRESHOLD:
            send_email(
                f'Subject: {self.mkt} Down {round(float_rate * 100, 2)}%\n\n{new_quote}'
            )
            new_quote['dayOpen'] = old_quote['dayOpen']
            self.record_quote(new_quote)
            print(f'[{time}] {self.mkt} Down {round(float_rate * 100, 2)}% | Alerting email sent | New quote recorded')
            return
