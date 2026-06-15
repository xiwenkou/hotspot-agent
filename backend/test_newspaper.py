import sys
sys.path.append('d:/game/backend')
from collectors.rss import RSSCollector

collector = RSSCollector("谷歌热点", "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans")
data = collector.fetch_data()
if data:
    print(f"Title: {data[0]['title']}")
    print(f"URL: {data[0]['url']}")
    print(f"Content length: {len(data[0]['rawHeat'])}")
    print(f"Content snippet: {data[0]['rawHeat'][:200]}")
