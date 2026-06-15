import feedparser
from typing import List, Dict, Any
from .base import BaseCollector
import ssl
from bs4 import BeautifulSoup

try:
    import newspaper
except ImportError:
    newspaper = None

# 解决某些 RSS 源证书验证问题
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

class RSSCollector(BaseCollector):
    def __init__(self, name: str, url: str):
        super().__init__()
        self.platform = name
        self.url = url

    def fetch_article_text(self, url: str) -> str:
        if not newspaper:
            return ""
        try:
            config = newspaper.Config()
            config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            config.request_timeout = 10
            
            import requests
            try:
                res = requests.get(url, headers={'User-Agent': config.browser_user_agent}, timeout=10, allow_redirects=True)
                final_url = res.url
                html = res.text
            except Exception:
                final_url = url
                html = ""

            article = newspaper.Article(final_url, config=config)
            if html:
                article.download(input_html=html)
            else:
                article.download()
                
            article.parse()
            text = article.text.strip()
            
            # 过滤无效提取结果
            if len(text) < 50 or "400." in text or "重定向" in text:
                return ""
                
            return text[:1500]
        except Exception:
            return ""

    def fetch_data(self) -> List[Dict[str, Any]]:
        try:
            feed = feedparser.parse(self.url)
            results = []
            
            # 取最新的前 10 篇文章作为“热点/最新情报”
            for rank, entry in enumerate(feed.entries[:10], start=1):
                title = entry.get("title", "").strip()
                link = entry.get("link", "")
                
                if not title:
                    continue
                
                real_text = ""
                # 尝试去它原网页里把真正的文章内容全扒下来
                real_text = self.fetch_article_text(link)

                # 如果无法提取到真实网页内容，降级回退到 RSS 的摘要
                if not real_text:
                    raw_summary = entry.get("summary", "") or entry.get("description", "")
                    real_text = BeautifulSoup(raw_summary, "html.parser").get_text(separator="\n", strip=True)
                
                content_payload = real_text[:1500] if real_text else "暂无内容"
                    
                results.append({
                    "title": title,
                    "platform": self.platform,
                    "url": link,
                    "author": None,
                    "publish_time": entry.get("published", ""),
                    "source_content": content_payload,
                    "html_snapshot": None,
                    "collected_at": self.get_current_time()
                })
            return results
        except Exception as e:
            print(f"获取 {self.platform} RSS失败: {e}")
            return []

if __name__ == "__main__":
    collector = RSSCollector("少数派", "https://sspai.com/feed")
    data = collector.fetch_data()
    print(f"成功获取 {len(data)} 条数据")
