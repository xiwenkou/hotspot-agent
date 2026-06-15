import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import RawArticle
from collectors.baidu import BaiduCollector
from collectors.zhihu import ZhihuCollector
from collectors.github import GithubCollector
from collectors.rss import RSSCollector
import time
from datetime import datetime

def fetch_all_platforms():
    print(f"[{datetime.now()}] 开始定时抓取任务...")
    db: Session = SessionLocal()
    collectors = [
        BaiduCollector(),
        ZhihuCollector(),
        GithubCollector(),
        RSSCollector("少数派", "https://sspai.com/feed")
    ]
    
    for collector in collectors:
        try:
            print(f"正在抓取: {collector.platform}")
            data = collector.fetch_data()
            for item in data:
                # 存入 RawArticle 表
                
                # 如果 publish_time 格式不正确，需要处理
                publish_time = item.get("publish_time")
                if isinstance(publish_time, str):
                    # 简单容错处理，如果不是datetime则置空
                    publish_time = None

                article = RawArticle(
                    title=item.get("title"),
                    platform=item.get("platform"),
                    url=item.get("url"),
                    author=item.get("author"),
                    publish_time=publish_time,
                    source_content=item.get("source_content"),
                    html_snapshot=item.get("html_snapshot"),
                    collected_at=item.get("collected_at")
                )
                db.add(article)
            db.commit()
            print(f"{collector.platform} 抓取完成，存入 {len(data)} 条数据")
        except Exception as e:
            db.rollback()
            print(f"{collector.platform} 抓取异常: {e}")
            
    db.close()
    print(f"[{datetime.now()}] 定时抓取任务完成.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # 每 30 分钟执行一次
    scheduler.add_job(fetch_all_platforms, 'interval', minutes=30)
    scheduler.start()
    print("调度器已启动，每 30 分钟触发一次抓取任务。")

if __name__ == "__main__":
    fetch_all_platforms() # 立即执行一次测试
