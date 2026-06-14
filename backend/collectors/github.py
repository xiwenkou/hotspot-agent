import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .base import BaseCollector

class GithubCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.platform = "GitHub Trending"
        self.url = "https://github.com/trending"

    def fetch_data(self) -> List[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        try:
            res = requests.get(self.url, headers=headers, timeout=10)
            res.raise_for_status()
            
            soup = BeautifulSoup(res.text, 'html.parser')
            repo_list = soup.find_all("article", class_="Box-row")
            
            results = []
            for rank, repo in enumerate(repo_list, start=1):
                h2 = repo.find("h2", class_="h3 lh-condensed")
                if not h2:
                    continue
                    
                a_tag = h2.find("a")
                title = a_tag.text.strip().replace(" ", "").replace("\n", "")
                url = "https://github.com" + a_tag.get("href", "")
                
                # 尝试获取 stars 数量
                stars_tag = repo.find("a", class_="Link--muted d-inline-block mr-3")
                heat = stars_tag.text.strip() if stars_tag else "未知stars"
                
                # 尝试获取描述作为一部分内容 (不过热点通常只需要标题，描述可以拼在标题后或丢弃)
                desc_tag = repo.find("p", class_="col-9 color-fg-muted my-1 pr-4")
                desc = desc_tag.text.strip() if desc_tag else ""
                
                full_title = f"{title}: {desc}" if desc else title

                results.append({
                    "title": full_title,
                    "platform": self.platform,
                    "url": url,
                    "rank": rank,
                    "rawHeat": f"{heat} stars",
                    "collectedAt": self.get_current_time()
                })
            return results
        except Exception as e:
            print(f"获取{self.platform}失败: {e}")
            return []

if __name__ == "__main__":
    collector = GithubCollector()
    data = collector.fetch_data()
    print(f"成功获取 {len(data)} 条数据")
    if data:
        print(data[0])
