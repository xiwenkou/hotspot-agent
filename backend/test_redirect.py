import requests
from bs4 import BeautifulSoup
import newspaper
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://news.google.com/rss/articles/CBMiNGh0dHBzOi8vd3d3LnBpbmd3ZXN0LmNvbS9hLzI5Mzg5M9IBAA?hl=zh-CN&gl=CN&ceid=CN%3Azh-Hans"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print("Fetching URL:", url)
res = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
print("Final URL:", res.url)

article = newspaper.Article(res.url)
article.download(input_html=res.text)
article.parse()
print("Content snippet:", article.text[:200])
