from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from pytrends.request import TrendReq
import grequests
from time import sleep
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd


def get_query(ind, topic, amt, unit, region):
    query_freq = defaultdict(int)

    pytrends = TrendReq(hl='en-US', tz=360)
    # pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})

    current_time = datetime.now()

    old_time = current_time

    if unit == "H":
        old_time = current_time - timedelta(hours=int(amt))
    elif unit == "D":
        old_time = current_time - timedelta(days=int(amt))
    elif unit == "M":
        old_time = current_time - timedelta(days=int(amt*30))
    elif unit == "Y":
        old_time = current_time - timedelta(days=int(amt * 365))

    print("Time frame:")
    print(str(old_time) + " " + str(current_time))

    kw_list = [topic]

    # converts datetime to date objects
    old_date = datetime.date(old_time)
    current_date = datetime.date(current_time)

    pytrends.build_payload(kw_list, cat=0, timeframe= str(old_date) + " " + str(current_date), geo=region, gprop='')

    interest_over_time = pytrends.interest_over_time()

    if interest_over_time.empty:
        return None

    largest_interest = interest_over_time.sort_values(by=[topic], ascending=False)

    largest_interest_dates = largest_interest.index

    # for index, row in pytrends.related_topics()[topic]['top'].iterrows():
    #     print(row)

    print(largest_interest)

    print("Day: " + str(largest_interest_dates[ind]))

    search_time = pd.Timestamp.to_pydatetime(largest_interest_dates[ind])
    search_date_first = datetime.date(search_time)
    search_date_second = datetime.date(search_time)

    # related_queries = pd.DataFrame(zip(pd.DataFrame(zip([],[]), columns=['top', 'rising'])),columns=[topic])
    related_queries = None
    cnt = 0

    while related_queries is None:
        cnt += 1
        search_date_first = search_date_first - timedelta(days=2)
        pytrends.build_payload(kw_list, cat=0, timeframe= str(search_date_first) + " " + str(search_date_second), geo=region, gprop='')
        related_queries = pytrends.related_queries()[topic]['top']

        if cnt > 5:
            break

    if related_queries is not None:
        print(search_date_first)
        print(search_date_second)

        print(related_queries)

        for index, row in related_queries.iterrows():
            if index > 9:
                break
            query_freq[row['query']] += row['value']

    return [search_date_first.strftime("%Y/%m/%d"), search_date_second.strftime("%Y/%m/%d"), sorted(query_freq.items(), key = lambda v: v[1], reverse=True), topic]


def get_sites(data):
    print(data)
    date = data[0]
    before = data[1]
    ret = []

    if len(data[2]) < 1:
        data[2] = [(data[3], 100)]
    news = []
    notnews = []
    for search, z in data[2]:
        if z > 70:
            search = search.replace(" ", "+")
            print("https://www.google.com/search?q=" + search + "+before:" + before + "+after:" + date)
            notnews.append("https://www.google.com/search?q=" + search + "+before:" + before + "+after:" + date)
            news.append("https://www.google.com/search?q=" + search + "+before:" + before + "+after:" + date + "&tbm=nws")

    print("beforemap")
    tmp = grequests.map((grequests.get(u) for u in notnews))
    print("aftermap")

    for page in tmp:
        # page = requests.get("https://www.google.com/search?q=" + search + "+before:" + before + "+after:" + date)
        # sleep(1)
        # print(page)

        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all("a")
        strlinks = []
        for i in links:
            st = i["href"][:7]
            if st == "/url?q=" and "youtube" not in i["href"] and ".google" not in i["href"]:
                if "&sa=" in i["href"]:
                    idx = i["href"].index("&sa=")
                else:
                    idx = len(st)
                strlinks.append([i["href"][7:idx],0])
        ret += strlinks[:2]

    print("beforemap")
    tmp2 = grequests.map((grequests.get(u) for u in news))
    print("aftermap")

    for page in tmp2:
        # page = requests.get("https://www.google.com/search?q=" + search + "+before:" + before + "+after:" + date + "&tbm=nws")
        # sleep(1)
        # print(page)

        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all("a")
        strlinks = []
        for i in links:
            st = i["href"][:7]
            if st == "/url?q=" and "youtube" not in i["href"] and ".google" not in i["href"]:
                if "&sa=" in i["href"]:
                    idx = i["href"].index("&sa=")
                else:
                    idx = len(st)
                strlinks.append([i["href"][7:idx],1])
        ret += strlinks[:1]
    print(ret)
    return ret


def search(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraphs = soup.find_all("p")
    txt = ""
    for i in paragraphs:
        txt += i.getText()
    return txt

def get_trending_list():
    pytrends = TrendReq(hl='en-US', tz=360)
    return pytrends.trending_searches(pn='united_states')[0][:7].values.tolist()


