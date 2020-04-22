import os
import json
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class RssNews:
    def __init__(self):
        self.url = 'https://finance.yahoo.com/rss/stock-market-news'
        self.refresh_interval = 60
    
    def load_xml_news(self):
        resp = requests.get(self.url) 
        return resp.content
    
    def parse_xml_news(self, s):
        tree = ET.ElementTree(ET.fromstring(s))
        root = tree.getroot()
        newsitems = [] 
        for item in root.findall('./channel/item'): 
            news = {} 
            for child in item: 
                if child.tag in ('{http://search.yahoo.com/mrss/}content', '{http://search.yahoo.com/mrss/}text', '{http://search.yahoo.com/mrss/}credit'):
                    continue
                elif child.tag == 'pubDate':
                    news[child.tag] = datetime.strptime(child.text, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d, %H:%M:%S')
                else:
                    news[child.tag] = child.text
            newsitems.append(news) 
        return sorted(newsitems, key = lambda x: x['pubDate'], reverse = True)

    def filter_news(self, newsitems):
        cut_off_time = (datetime.now() - timedelta(minutes = self.refresh_interval)).strftime('%Y-%m-%d, %H:%M:%S')
        filtered_news = []
        for news in newsitems:
            if news['pubDate'] >= cut_off_time:
                filtered_news.append(news)
        return filtered_news
    
class WebpageNews:
    def __init__(self):
        self.url = 'https://finance.yahoo.com/topic/stock-market-news'
        self.news_records_path = 'archive/news/' + datetime.now().strftime('%Y%m') + '/' + datetime.now().strftime('%Y%m%d') + '.news'
        if os.getenv('VERSION') == 'production':
            self.news_records_path = '/home/ec2-user/ASMAT/' + self.news_records_path

    def get_response(self):
        rsp = requests.get(self.url)
        return rsp
    
    def parse_news_items(self, html):
        soup = BeautifulSoup(html.text, 'html.parser')
        news_containers = soup.find_all('div', class_ = 'Py(14px) Pos(r)')
        archived_news = self.load_news_records()
        news_items = []
        time = datetime.now().strftime('%Y-%m-%d %H:%M')
        if not archived_news:
            for news in news_containers:
                item = {}
                item['title'] = news.find('a').text
                item['description'] = news.find('p').text
                item['href'] = 'https://finance.yahoo.com' + news.find('a')['href']
                item['source'] = news.find('div', class_ = 'C(#959595) Fz(11px) D(ib) Mb(6px)').text
                item['time'] = time
                news_items.append(item)
            archived_news = list(reversed(news_items))
            self.write_news(archived_news)
            return news_items
        else:
            last_news_title = archived_news[-1]['title']
            for news in news_containers:
                item = {}
                item['title'] = news.find('a').text
                item['description'] = news.find('p').text
                item['href'] = 'https://finance.yahoo.com' + news.find('a')['href']
                item['source'] = news.find('div', class_ = 'C(#959595) Fz(11px) D(ib) Mb(6px)').text
                item['time'] = time
                if item['title'] == last_news_title:
                    break
                news_items.append(item)
            archived_news += list(reversed(news_items))
            self.write_news(archived_news)
            return news_items
    
    def load_news_records(self):
        if not os.path.exists(self.news_records_path):
            return None
        try:
            with open(self.news_records_path) as json_file:
                news_records = json.load(json_file)
            return news_records
        except:
            return None
    
    def write_news(self, news_to_write):
        if not os.path.exists(self.news_records_path):
            os.makedirs(os.path.dirname(self.news_records_path))
        with open(self.news_records_path, 'w', encoding = 'utf-8') as json_file:
            json.dump(news_to_write, json_file, indent = 4)
        


