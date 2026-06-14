import requests
import re
import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .base import BaseCollector

class ZhihuCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.platform = "知乎热榜"
        self.url = "https://www.zhihu.com/billboard"

    def fetch_data(self) -> List[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        try:
            res = requests.get(self.url, headers=headers, timeout=10)
            res.raise_for_status()
            
            # 知乎将初始化数据嵌在 <script id="js-initialData" type="text/json"> 里
            match = re.search(r'<script id="js-initialData" type="text/json">(.*?)</script>', res.text)
            if not match:
                print("知乎热榜未找到初始数据块")
                return []
                
            data = json.loads(match.group(1))
            
            # 知乎的新版初始数据结构可能变化，尝试通过几个已知路径找数据
            hot_list = []
            try:
                hot_list = data["initialState"]["topstory"]["hotList"]
            except KeyError:
                pass
                
            results = []
            if hot_list:
                for rank, item in enumerate(hot_list, start=1):
                    target = item.get("target", {})
                    title = target.get("titleArea", {}).get("text", "")
                    link = target.get("link", {}).get("url", "")
                    heat = target.get("metricsArea", {}).get("text", "")
                    
                    if not title:
                        continue
                        
                    results.append({
                        "title": title,
                        "platform": self.platform,
                        "url": link,
                        "rank": rank,
                        "rawHeat": heat,
                        "collectedAt": self.get_current_time()
                    })
            return results
        except Exception as e:
            print(f"获取{self.platform}失败: {e}")
            return []

if __name__ == "__main__":
    collector = ZhihuCollector()
    data = collector.fetch_data()
    print(f"成功获取 {len(data)} 条数据")
    if data:
        print(json.dumps(data[0], ensure_ascii=False, indent=2))
