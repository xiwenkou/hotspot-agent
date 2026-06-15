from sqlalchemy.orm import Session
from models import models
from typing import List, Dict, Any
from datetime import datetime, timedelta

class HotEventService:
    def __init__(self, db: Session):
        self.db = db

    def get_today_events(self, limit: int = 20):
        """获取最新的热点事件。第一阶段重构中，我们先直接返回最近抓取的 RawArticle 假装为 HotEvent 展示"""
        yesterday = datetime.utcnow() - timedelta(days=1)
        raw_articles = self.db.query(models.RawArticle).filter(
            models.RawArticle.collected_at >= yesterday
        ).order_by(models.RawArticle.collected_at.desc()).limit(limit).all()
        
        results = []
        for article in raw_articles:
            # 临时适配前端所期望的格式，第二阶段再由 AgentInsight 真正提供这些字段
            is_github = "github" in article.platform.lower()
            category = "github" if is_github else "news"
            
            results.append({
                "id": article.id,
                "title": article.title,
                "summary": (article.source_content[:100] + "...") if article.source_content else "无正文",
                "category": category,
                "platforms": [article.platform],
                "credibility": "暂无评级",
                "risk_level": "等待Agent分析",
                "creative_value": 0,
                "tags": [article.platform],
                "angles": [],
                "suggestion": "等待Agent分析"
            })
            
        return results
