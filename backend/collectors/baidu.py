import requests
import re
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .base import BaseCollector

class BaiduCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.platform = "百度热搜"
        self.url = "https://top.baidu.com/board?tab=realtime"

    def fetch_data(self) -> List[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            res = requests.get(self.url, headers=headers, timeout=10)
            res.raise_for_status()
            
            # 使用正则提取页面内嵌的 JSON 数据
            match = re.search(r'<!--s-data:(.*?)-->', res.text, re.S)
            if not match:
                print("百度热搜未找到数据块")
                return []
                
            data = json.loads(match.group(1))
            cards = data.get("data", {}).get("cards", [])
            
            results = []
            if cards:
                # 百度热搜的数据通常在 cards[0]['content']
                items = cards[0].get("content", [])
                for rank, item in enumerate(items, start=1):
                    title = item.get("word", "")
                    url = item.get("appUrl", "")
                    hot_score = str(item.get("hotScore", ""))
                    desc = item.get("desc", "")
                    
                    if not title:
                        continue
                        
                    # 尝试抓取原文
                    source_content = self.fetch_article_text(url)
                    if not source_content:
                        source_content = desc if desc else f"当前热度：{hot_score}"
                        
                    results.append({
                        "title": title,
                        "platform": self.platform,
                        "url": url,
                        "author": None,
                        "publish_time": None,
                        "source_content": source_content,
                        "html_snapshot": None,
                        "collected_at": self.get_current_time()
                    })
            return results
        except Exception as e:
            print(f"获取{self.platform}失败: {e}")
            return []

if __name__ == "__main__":
    collector = BaiduCollector()
    data = collector.fetch_data()
    print(f"成功获取 {len(data)} 条数据")
    if data:
        print(json.dumps(data[0], ensure_ascii=False, indent=2))
