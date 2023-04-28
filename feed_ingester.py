import feedparser

def feed_ingester(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries
