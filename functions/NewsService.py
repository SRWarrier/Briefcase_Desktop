import feedparser




def getNews():
    url = 'https://www.livemint.com/rss/news'
    Feed = feedparser.parse(url)
    entries = Feed['entries']
    Deck = []
    counter = 0
    for entry in entries:
        Title = entry['title']
        Summary = entry['summary']
        Text = Title+'\n'+Summary
        Deck.append({'description':Text, pdf:entry['link']})
        counter+=1
        if counter==20:
            break
    return Deck


