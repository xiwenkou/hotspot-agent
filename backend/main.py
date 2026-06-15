from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db, Base, engine
from models import models
from services.hot_event_service import HotEventService
from tasks.scheduler import start_scheduler
from contextlib import asynccontextmanager

# 确保表结构已建立
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行
    start_scheduler()
    yield
    # 应用关闭时执行可以关闭 scheduler，暂略

app = FastAPI(title="热点情报 Agent API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to Hotspot Agent API"}

@app.get("/api/hot-events/today")
def get_today_events(limit: int = Query(20, ge=1, le=50), db: Session = Depends(get_db)):
    """获取今日热门事件列表"""
    service = HotEventService(db)
    events = service.get_today_events(limit=limit)
    return {
        "code": 200,
        "message": "success",
        "data": events
    }

@app.get("/api/hot-events")
def get_events_by_category(category: Optional[str] = None, limit: int = 20, db: Session = Depends(get_db)):
    """根据分类筛选热点事件（第一阶段暂不实现，直接复用 get_today_events）"""
    service = HotEventService(db)
    events = service.get_today_events(limit=limit)
    if category:
        events = [e for e in events if e.get("category") == category]
    return {
        "code": 200,
        "message": "success",
        "data": events
    }

@app.get("/api/hot-events/{event_id}")
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """获取单条热点事件详情。第一阶段暂时返回 RawArticle 数据"""
    article = db.query(models.RawArticle).filter(models.RawArticle.id == event_id).first()
    if not article:
        return {"code": 404, "message": "事件不存在", "data": None}
    
    is_github = "github" in article.platform.lower()
    
    data = {
        "id": article.id,
        "title": article.title,
        "summary": article.source_content if article.source_content else "无正文",
        "category": "github" if is_github else "news",
        "platforms": [article.platform],
        "credibility": "暂无评级",
        "risk_level": "等待Agent分析",
        "creative_value": 0,
        "tags": [article.platform],
        "angles": [],
        "suggestion": "等待Agent分析",
        "url": article.url,
        "publish_time": article.publish_time
    }
    
    return {
        "code": 200,
        "message": "success",
        "data": data
    }
