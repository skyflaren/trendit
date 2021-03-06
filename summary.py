from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
# from summa.summarizer import summarize
# from summa.keywords import keywords
from newspaper import Article
import nltk
from retrieve_trends import *

def get_results(topic, amt, unit, region):
    topic = topic.strip()

    links = []

    for i in range(3):
        query = get_query(i, topic, amt, unit, "" if region == "WW" else region)
        if query is not None:
            # print("No large events found, please try refining your search terms")
            links += get_sites(query)

    entries = []
    news = []
    notnews = []
    for link, val in links:
        if link not in news and link not in notnews:
            if val:
                news.append(link)
            else:
                notnews.append(link)
    for idx, link in enumerate(news):
    # for idx, link in enumerate(grequests.map((grequests.get(u) for u in news))):
        # text = search(link)
        # summary = summarize(text, words=150)
        summary = ""
        try:
            article = Article(link)

            article.download()
            article.parse()
            article.nlp()
            summary = article.summary
            # if "Cloudflare" in summary:
            #     print("Cloudflare")
            #     summary = ""
        except:
            pass
        entries.append([news[idx], summary])
    for link in notnews:
        entries.append([link, ""])

    # for link, val in links:
    #     if link not in visited:
    #         text = search(link)
    #         visited.add(link)
    #         summary = ""
    #         if len(text) < 8000 and val == 1:
    #             summary = summarize(text, words=100)
    #
    #         entries.append([link, summary])
    # for l,s in entries:
    #     print(l)
    #     print(s)
    if len(entries) == 0:
        entries.append(["", "No large events were found, please try refining your search terms or increasing your time range."])
    return entries


# get_results("samsung","1","Y","WW")
