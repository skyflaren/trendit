from summa.summarizer import summarize
from summa.keywords import keywords
from retrieve_trends import *

topic = input("What would you like to search for? ")

timeframe = ""
options = ["1-y","1-m","7-d"]

# gets time frame input
while timeframe not in options:
    timeframe = input("Select a timeframe (1-y, 1-m, 7-d): ")

links = []

for i in range(3):
    query = get_query(i, topic, timeframe)
    if query is None:
        print("No large events found, please try refining your search terms")
    else:
        links += get_sites(query)

links = set(links)
for link in links:
    text = search(link)
    if len(text) < 5000:
        print(link)
        print(keywords(text))
        print(summarize(text, 0.15))
