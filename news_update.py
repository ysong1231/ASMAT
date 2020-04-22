from datetime import datetime
from core.News import WebpageNews
from common_tools.send_email import send_email
from common_tools.format_email_content import format_news_alert

news = WebpageNews()
html_response = news.get_response()
newsitems = news.parse_news_items(html_response)
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f'[{time}] {len(newsitems)} piece of news updated')

if newsitems:
    send_email('Subject: Recent News:'+ '\n\n' + format_news_alert(newsitems))