import json
import time
from database import SessionLocal, engine, Base
from models import models
from services.hot_event_service import HotEventService
from collectors import BaiduCollector, ZhihuCollector, GithubCollector
from agents.analyzer_agent import AnalyzerAgent

def main():
    print("=== 开始第二阶段：数据采集与入库测试 ===\n")
    
    # 确保数据库表存在
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    service = HotEventService(db)
    
    # 1. 初始化采集器
    collectors = [
        BaiduCollector(),
        GithubCollector()
    ]
    
    all_raw_data = []
    
    # 2. 采集数据
    for collector in collectors:
        print(f"正在从 [{collector.platform}] 采集数据...")
        data = collector.fetch_data()
        print(f"[{collector.platform}] 成功采集 {len(data)} 条数据。\n")
        
        # 存入原始数据表 (每个取前3条演示)
        sample_data = data[:3]
        all_raw_data.extend(sample_data)
        time.sleep(1)
        
    print(f"正在将 {len(all_raw_data)} 条原始数据存入 raw_hot_items 表...")
    service.save_raw_items(all_raw_data)
        
    print(f"\n=== 开始进行 AI 分析并入库 (hot_events 表) ===\n")
    
    # 3. 初始化 Agent 并分析
    agent = AnalyzerAgent()
    
    for i, event in enumerate(all_raw_data, start=1):
        print(f"正在分析并保存第 {i} 条热点: {event['title']}")
        # 调用大模型
        analyzed_data = agent.analyze_event(event)
        
        # 保存到热点事件表（含简单的合并逻辑）
        saved_event = service.save_analyzed_event(analyzed_data)
        print(f"  -> 入库成功，事件ID: {saved_event.id}, 目前涉及平台: {saved_event.platforms}")
        time.sleep(1)
        
    # 4. 验证查询
    print("\n=== 验证数据库查询: 获取最新事件 ===")
    recent_events = service.get_today_events(limit=5)
    for ev in recent_events:
        print(f"ID:{ev.id} | [{ev.category}] {ev.title} (风险:{ev.risk_level})")

    db.close()
    print("\n=== 第二阶段数据入库链路测试完成 ===")

if __name__ == "__main__":
    main()
