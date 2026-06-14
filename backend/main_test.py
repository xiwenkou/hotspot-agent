import json
import time
from collectors import BaiduCollector, ZhihuCollector, GithubCollector
from agents import AnalyzerAgent

def main():
    print("=== 开始第一阶段：核心链路测试 ===\n")
    
    # 1. 初始化采集器
    collectors = [
        BaiduCollector(),
        GithubCollector(),
        ZhihuCollector()
    ]
    
    all_hot_events = []
    
    # 2. 采集数据
    for collector in collectors:
        print(f"正在从 [{collector.platform}] 采集数据...")
        data = collector.fetch_data()
        print(f"[{collector.platform}] 成功采集 {len(data)} 条数据。\n")
        
        # 为了测试，每个平台只取前 2 条
        all_hot_events.extend(data[:2])
        time.sleep(1) # 避免请求过快
        
    print(f"=== 采集完成，共选取 {len(all_hot_events)} 条数据进行 AI 分析 ===\n")
    
    # 3. 初始化 Agent
    agent = AnalyzerAgent()
    if not agent.api_key:
        print("!! 注意: DEEPSEEK_API_KEY 未设置，Agent 将无法进行分析。请在 .env 文件中设置。")
        
    analyzed_results = []
    
    # 4. Agent 分析
    for i, event in enumerate(all_hot_events, start=1):
        print(f"正在分析第 {i} 条热点: {event['title']}")
        result = agent.analyze_event(event)
        analyzed_results.append(result)
        time.sleep(1) # 避免 API 频率限制
        
    # 5. 输出结果
    print("\n=== AI 分析结果展示 ===")
    print(json.dumps(analyzed_results, ensure_ascii=False, indent=2))
    
    print("\n=== 第一阶段核心链路跑通测试完成 ===")

if __name__ == "__main__":
    main()
