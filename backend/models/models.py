from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class PlatformSource(Base):
    __tablename__ = "platform_sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    url = Column(String)
    enabled = Column(Boolean, default=True)
    
class RawArticle(Base):
    __tablename__ = "raw_articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    platform = Column(String, index=True)
    url = Column(String)
    author = Column(String, nullable=True)
    publish_time = Column(DateTime, nullable=True)
    source_content = Column(Text, nullable=True) # 真正抓取到的原文
    html_snapshot = Column(Text, nullable=True)  # 原始的 HTML 备份（可选）
    
    event_id = Column(Integer, ForeignKey("hot_events.id"), nullable=True)
    collected_at = Column(DateTime, default=datetime.utcnow)

class HotEvent(Base):
    __tablename__ = "hot_events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True) # 去重后的核心标题
    category = Column(String, index=True)
    
    # 汇总的热度数据
    platforms = Column(JSON) # 包含该事件的平台列表
    heat_index = Column(Float, default=0.0) # 根据跨平台及排名计算的热度指数
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    raw_articles = relationship("RawArticle", backref="event")
    insight = relationship("AgentInsight", backref="event", uselist=False)

class AgentInsight(Base):
    __tablename__ = "agent_insights"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("hot_events.id"), unique=True)
    
    agent_summary = Column(Text, nullable=True) # AI 对所有相关原文的总结摘要
    risk_level = Column(String) # 高、中、低等
    creative_value = Column(Integer) # 创作价值评分 (1-10)
    angles = Column(JSON, nullable=True) # 建议的创作切入点
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PushTask(Base):
    __tablename__ = "push_tasks"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("hot_events.id"), nullable=True)
    push_type = Column(String) # 例如 'morning_report', 'urgent' 等
    status = Column(String, default="pending") # pending, pushed, failed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    pushed_at = Column(DateTime, nullable=True)
