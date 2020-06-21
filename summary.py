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

visited = set()

entries = []

for link, val in links:
    if link not in visited:
        text = search(link)
        visited.add(link)
        summary = ""
        if len(text) < 8000 and val == 1:
            summary = summarize(text, words=100)

        entries.append([link, summary])

for l, s in entries:
    print(l)
    print(s)

