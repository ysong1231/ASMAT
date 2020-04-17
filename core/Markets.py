import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Markets:
    def __init__(self, markets):
        self.url = 'https://financialmodelingprep.com/api/v3/quote/' + ','.join([markets[m] for m in markets])
        self.FLOAT_THRESHOLD = 0.0025
        self.markets = markets
        if os.getenv('VERSION') == 'local':
            self.conf_path = 'conf/markets_records.json'
        if os.getenv('VERSION') == 'production':
            self.conf_path = '/home/ec2-user/ASMAT/conf/markets_records.json'
        
    def get_quote(self):
        with requests.Session() as s:
            request = s.get(self.url, timeout=15)
            quote_data = request.json()
        return quote_data
    
    def load_record(self):
        with open(self.conf_path) as json_file:
            quote_record = json.load(json_file)
        return quote_record
    
    def write_records(self, q):
        with open(self.conf_path, 'w') as json_file:
            json.dump(q, json_file, indent=4)
    
    def ts_to_date(self, ts):
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

    def real_time_check(self):
        new_quote = self.get_quote()
        records = self.load_record()
        alerts = []
        for i, idx in enumerate(self.markets):
            if self.ts_to_date(new_quote[i]['timestamp']) != self.ts_to_date(records[idx]['timestamp']):
                records[idx]['dayOpen'] = new_quote[i]['price']
                records[idx]['price'] = new_quote[i]['price']
                records[idx]['lastAlertPrice'] = new_quote[i]['price']
                records[idx]['last_max'] = new_quote[i]['price']
                records[idx]['last_min'] = new_quote[i]['price']
                records[idx]['timestamp'] = new_quote[i]['timestamp']
                records[idx]['lastAlertTimestamp'] = new_quote[i]['timestamp']
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'[{time}] {idx} open price recorded')
                continue
            
            change_from_last_alert = (new_quote[i]['price'] - records[idx]['lastAlertPrice']) / records[idx]['dayOpen']
            change_from_last_max = (new_quote[i]['price'] - records[idx]['last_max']) / records[idx]['dayOpen']
            change_from_last_mim = (new_quote[i]['price'] - records[idx]['last_min']) / records[idx]['dayOpen']

            if change_from_last_alert >= self.FLOAT_THRESHOLD or change_from_last_mim >= self.FLOAT_THRESHOLD:
                float_rate = min(change_from_last_alert, change_from_last_mim)
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'[{time}] {idx} Up {round(float_rate * 100, 2)}%')
                records[idx]['price'] = new_quote[i]['price']
                records[idx]['lastAlertPrice'] = new_quote[i]['price']
                records[idx]['last_max'] = new_quote[i]['price']
                records[idx]['last_min'] = new_quote[i]['price']
                records[idx]['timestamp'] = new_quote[i]['timestamp']
                records[idx]['lastAlertTimestamp'] = new_quote[i]['timestamp']
                alerts.append(f'{idx} Up {round(float_rate * 100, 2)}%')
                continue

            if change_from_last_alert <= -self.FLOAT_THRESHOLD or change_from_last_max <= -self.FLOAT_THRESHOLD:
                float_rate = min(change_from_last_alert, change_from_last_max)
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'[{time}] {idx} Down {round(float_rate * 100, 2)}%')
                records[idx]['price'] = new_quote[i]['price']
                records[idx]['lastAlertPrice'] = new_quote[i]['price']
                records[idx]['last_max'] = new_quote[i]['price']
                records[idx]['last_min'] = new_quote[i]['price']
                records[idx]['timestamp'] = new_quote[i]['timestamp']
                records[idx]['lastAlertTimestamp'] = new_quote[i]['timestamp']
                alerts.append(f'{idx} Down {round(float_rate * 100, 2)}%')
                continue

            records[idx]['price'] = new_quote[i]['price']
            records[idx]['last_max'] = max(new_quote[i]['price'], records[idx]['last_max'])
            records[idx]['last_min'] = min(new_quote[i]['price'], records[idx]['last_min'])
            records[idx]['timestamp'] = new_quote[i]['timestamp']
            continue

        self.write_records(records)
        return alerts, new_quote