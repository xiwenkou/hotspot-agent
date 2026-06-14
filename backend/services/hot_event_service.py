from sqlalchemy.orm import Session
from models import models
from typing import List, Dict, Any

class HotEventService:
    def __init__(self, db: Session):
        self.db = db

    def save_raw_items(self, items: List[Dict[str, Any]]):
        """批量保存原始抓取的数据"""
        raw_items = []
        for item in items:
            raw_item = models.RawHotItem(
                title=item.get("title"),
                platform=item.get("platform"),
                url=item.get("url"),
                rank=item.get("rank"),
                raw_heat=item.get("rawHeat")
            )
            raw_items.append(raw_item)
            
        if raw_items:
            self.db.add_all(raw_items)
            self.db.commit()

    def save_analyzed_event(self, analyzed_data: Dict[str, Any]):
        """保存经过 AI 分析后的热点事件，并做简单的名称去重合并"""
        title = analyzed_data.get("title")
        platform = analyzed_data.get("platform")
        
        # 简单根据标题查询是否已有事件
        existing_event = self.db.query(models.HotEvent).filter(models.HotEvent.title == title).first()
        
        if existing_event:
            # 如果存在，更新平台信息和热度（合并逻辑）
            platforms = existing_event.platforms or []
            if platform not in platforms:
                platforms.append(platform)
            
            existing_event.platforms = platforms
            
            # 取最高排名（数字越小排名越高）
            current_rank = analyzed_data.get("rank", 999)
            if current_rank < existing_event.max_rank:
                existing_event.max_rank = current_rank
                
            self.db.commit()
            self.db.refresh(existing_event)
            return existing_event
        else:
            # 新建事件
            new_event = models.HotEvent(
                title=title,
                summary=analyzed_data.get("summary"),
                category=analyzed_data.get("category"),
                tags=analyzed_data.get("tags", []),
                credibility=analyzed_data.get("credibility"),
                risk_level=analyzed_data.get("riskLevel"),
                creative_value=analyzed_data.get("creativeValue"),
                angles=analyzed_data.get("angles", []),
                suggestion=analyzed_data.get("suggestion"),
                max_rank=analyzed_data.get("rank", 999),
                platforms=[platform]
            )
            self.db.add(new_event)
            self.db.commit()
            self.db.refresh(new_event)
            return new_event

    def get_today_events(self, limit: int = 20):
        """获取最新的热点事件"""
        return self.db.query(models.HotEvent).order_by(models.HotEvent.created_at.desc()).limit(limit).all()
