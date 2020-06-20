from pytrends.request import TrendReq
from datetime import datetime
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360)
# pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})

topic = input("What would you like to search for? ")
current_time = datetime.now()

timeframe = ""
options = ["1-y","1-m","1-d"]

# gets time frame input
while timeframe not in options:
    timeframe = input("Select a timeframe (1-y, 1-m, 7-d): ")

old_time = current_time

if timeframe == "1-y":
    old_time = datetime(current_time.year - 1, current_time.month, current_time.day)

print(str(old_time) + " " + str(current_time))

kw_list = [topic]

# converts datetime to date objects
old_date = datetime.date(old_time)
current_date = datetime.date(current_time)

pytrends.build_payload(kw_list, cat=0, timeframe= str(old_date) + " " + str(current_date), geo='', gprop='')

interest_over_time = pytrends.interest_over_time()

largest_interest = interest_over_time.sort_values(by=[topic], ascending=False)

largest_interest_dates = largest_interest.index

print(type(largest_interest_dates[0]))
print(largest_interest_dates[0])

search_time = pd.Timestamp.to_pydatetime(largest_interest_dates[0])
search_date = datetime.date(search_time)

pytrends.build_payload(kw_list, cat=0, timeframe= str(search_date) + " " + str(search_date), geo='', gprop='')

print(pytrends.related_queries()[topic]['rising']['query'])
