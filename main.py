from core.Quotes import Quotes

sp500 = Quotes('S&P500')
#print(sp500.load_last_quote())
sp500.real_time_check()