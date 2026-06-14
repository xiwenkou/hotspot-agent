from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db, Base, engine
from models import models
from services.hot_event_service import HotEventService

# 确保表结构已建立
Base.metadata.create_all(bind=engine)

app = FastAPI(title="热点情报 Agent API", version="1.0.0")

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
    """根据分类筛选热点事件"""
    query = db.query(models.HotEvent)
    if category:
        query = query.filter(models.HotEvent.category == category)
    
    events = query.order_by(models.HotEvent.created_at.desc()).limit(limit).all()
    return {
        "code": 200,
        "message": "success",
        "data": events
    }

@app.get("/api/hot-events/{event_id}")
def get_event_detail(event_id: int, db: Session = Depends(get_db)):
    """获取单条热点事件详情"""
    event = db.query(models.HotEvent).filter(models.HotEvent.id == event_id).first()
    if not event:
        return {"code": 404, "message": "事件不存在", "data": None}
    
    return {
        "code": 200,
        "message": "success",
        "data": event
    }
