from datetime import datetime
from core.News import WebpageNews
# from common_tools.send_email import send_email
# from common_tools.format_email_content import format_news_alert

news = WebpageNews()
n = news.collect()

time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f'[{time}] {n} pieces of news updated!')

#if newsitems:
#    send_email('Subject: Recent News:'+ '\n\n' + format_news_alert(newsitems))