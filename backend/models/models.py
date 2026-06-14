from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Float
from datetime import datetime
from database import Base

class HotEvent(Base):
    __tablename__ = "hot_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True) # 去重后的核心标题
    summary = Column(Text, nullable=True)
    category = Column(String, index=True)
    tags = Column(JSON, nullable=True) # 以 JSON 格式存储标签列表
    
    # AI 评估字段
    credibility = Column(String)
    risk_level = Column(String)
    creative_value = Column(Integer)
    angles = Column(JSON, nullable=True)
    suggestion = Column(Text, nullable=True)
    
    # 热度数据 (为了简化，我们将原始热度汇总展示)
    max_rank = Column(Integer, default=999)
    platforms = Column(JSON) # 包含该事件的平台列表
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RawHotItem(Base):
    __tablename__ = "raw_hot_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    platform = Column(String, index=True)
    url = Column(String)
    rank = Column(Integer)
    raw_heat = Column(String)
    
    # 如果关联到了具体的热点事件，则记录 ID
    event_id = Column(Integer, nullable=True)
    
    collected_at = Column(DateTime, default=datetime.utcnow)
