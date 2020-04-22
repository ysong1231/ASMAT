from core.Markets import Markets
from common_tools.send_email import send_email
from common_tools.format_email_content import format_market_alert

markets = {
    'DOW': '%5EDJI',
    'S&P500': '%5EGSPC',
    'NASDAQ': '%5EIXIC'
}
idx = Markets(markets)
alerts, quotes = idx.real_time_check()
if alerts:
    send_email('Subject:'+ ', '.join(alerts) + '\n\n' + format_market_alert(quotes))
