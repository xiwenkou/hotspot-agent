from typing import List, Dict, Any
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
            "rank": 1,
            "rawHeat": "热度字符串",
            "collectedAt": "YYYY-MM-DD HH:MM:SS"
        }
        """
        pass

    def get_current_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
