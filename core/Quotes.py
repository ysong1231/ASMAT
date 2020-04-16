import json
import requests
from datetime import datetime
from common_tools.send_email import send_email

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
        self.mkt = market_index
        self.FLOAT_THRESHOLD = 0.01
        self.REPORT_FREQUENCY = 60

    def get_quote(self):
        with requests.Session() as s:
            request = s.get(self.url, timeout=15)
            quote_data = request.json()[0]
        return quote_data
    
    def load_last_quote(self):
        with open('conf/.quotes.json') as json_file:
            last_quote = json.load(json_file)
        return last_quote
    
    def record_quote(self, q):
        with open('conf/.quotes.json', 'w') as json_file:
            json.dump(q, json_file)
    
    def ts_to_date(self, ts):
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

    def real_time_check(self):
        new_quote = self.get_quote()
        old_quote = self.load_last_quote()
        float_rate = (new_quote.get('price') - old_quote.get('price')) / new_quote.get('open')

        if self.ts_to_date(new_quote.get('timestamp')) != self.ts_to_date(old_quote.get('timestamp')):
            self.record_quote(new_quote)
            return

        if new_quote.get('dayHigh') > old_quote.get('dayHigh') \
            or new_quote.get('dayLow') < old_quote.get('dayLow') \
            or abs(float_rate) >= self.FLOAT_THRESHOLD:
            self.record_quote(new_quote)
            print('New quote recorded')

        if abs(float_rate) >= self.FLOAT_THRESHOLD:
            if float_rate < 0:
                send_email(
                    f"""
                    Subject: {self.mkt} Down {float_rate}
                    {new_quote}
                    """)
            if float_rate > 0:
                send_email(
                    f'Subject: {self.mkt} Up {float_rate} \
                    {new_quote}'
                    )
            print('Email Sent')
