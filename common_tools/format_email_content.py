import json

def format_json(j):
    return(json.dumps(j, indent=4))

def format_market_alert(c):
    return '\n========================\n'.join(map(format_json, c))

def format_news_alert(newsitems):
    return '\n========================\n'.join(['\n'.join([news['title'], news['href']]) for news in newsitems])