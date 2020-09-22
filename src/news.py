import requests
import time
from datetime import datetime
import pandas as pd

API_KEY = ""
#YYYY-MM-DD
def get_news(companies_list):
    news_list = []
    current_time = int(time.time())
    last_time = current_time - 7*24*60*60

    to_date = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d')
    from_date = datetime.fromtimestamp(last_time).strftime('%Y-%m-%d')

    #company news
    for company in companies_list:
        r = requests.get('https://finnhub.io/api/v1/company-news?symbol=' + company.ticker + '&from=' + from_date + '&to=' + to_date + '&token=' + API_KEY)
        if len(r.json()) > 0:
            news_list.append(r.json()[0])
    
    #general news
    categs = ["general", "crypto"]
    for categ in categs:
        r = requests.get('https://finnhub.io/api/v1/news?category=' + categ + '&token=' + API_KEY)
        if len(r.json()) > 0:
            news_list.append(r.json()[0])

    ##we only want to keep:
    #out of -> category, datetime, headline, id, image, related, source, summary, url

    return news_list

    
