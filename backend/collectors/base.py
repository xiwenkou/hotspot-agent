from typing import List, Dict, Any, Optional
from datetime import datetime
import abc

class BaseCollector(abc.ABC):
    """
    数据采集器基类
    """
    def __init__(self):
        self.platform = "未知平台"

    @abc.abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        """
        核心方法：获取平台数据并返回标准化格式的列表
        格式如下：
        {
            "title": "热点标题",
            "platform": "平台名称",
            "url": "来源链接",
            "author": "作者或发布者(可选)",
            "publish_time": "发布时间(可选，datetime对象或字符串)",
            "source_content": "抓取到的原文文本",
            "html_snapshot": "原始HTML文本(可选)",
            "collected_at": datetime对象
        }
        """
        pass

    def fetch_article_text(self, url: str) -> str:
        """尝试抓取网页正文"""
        try:
            import newspaper
        except ImportError:
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
            
            if len(text) < 50 or "400." in text or "重定向" in text:
                return ""
            return text[:3000] # 截取前3000字作为原文内容
        except Exception:
            return ""

    def get_current_time(self) -> datetime:
        return datetime.utcnow()

