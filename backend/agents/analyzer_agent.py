import os
import json
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# 使用 pydantic 定义期望的输出结构（如果模型支持 structured outputs，但 deepseek 目前主要用 json mode 甚至直接 prompt 约定）
class HotEventAnalysis(BaseModel):
    summary: str = Field(description="100字以内的摘要")
    category: str = Field(description="事件分类，从以下选择: 科技、AI、iOS/移动开发、GIS/地图/定位、校园、社会、娱乐、游戏、国际、财经、网文/内容创作、其他")
    tags: List[str] = Field(description="关键词标签列表")
    credibility: str = Field(description="可信度等级: 未验证、有媒体报道、有官方回应、多方确认、存在争议、已反转")
    riskLevel: str = Field(description="风险等级: 低、中、高")
    creativeValue: int = Field(description="创作价值评分 (1-10)")
    angles: List[str] = Field(description="3个可创作角度")
    suggestion: str = Field(description="跟进建议")

class AnalyzerAgent:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            print("警告: 环境变量 DEEPSEEK_API_KEY 未设置！")
        
        # DeepSeek API 兼容 OpenAI SDK
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        self.model_name = "deepseek-chat" # 或 deepseek-reasoner

    def analyze_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        对单条热点数据进行分析
        """
        if not self.api_key:
            return {"error": "未配置 DEEPSEEK_API_KEY"}

        platform = event_data.get('platform', '')
        if "百度" in platform or "谷歌" in platform:
            # 执行零干预原味直出逻辑 (Passthrough)
            raw_content = event_data.get("rawHeat", "")
            return {
                "title": event_data.get("title"),
                "platform": platform,
                "url": event_data.get("url"),
                "rank": event_data.get("rank"),
                "summary": raw_content if raw_content else "无详细原文摘要",
                "category": "实时热点",
                "tags": [platform],
                "credibility": "原始数据",
                "riskLevel": "未知",
                "creativeValue": 0,
                "angles": [],
                "suggestion": ""
            }

        prompt = f"""
你是一个专业的深度热点分析 Agent。

请根据以下热点标题、正文摘要和来源平台，生成结构化分析。

要求：
1. 不要编造没有来源的信息；
2. 摘要（summary）必须是一段 300~500 字的、富有细节的深度背景剖析与概括，不要只是一句话结论，要把事件的前因后果、关键数据、核心争议或技术细节都写出来；
3. 判断事件分类；
4. 判断可信度；
5. 判断反转风险；
6. 给出 3 个可创作角度；
7. 输出严格的 JSON，不要输出 Markdown 代码块，不要有多余解释。

分类只能从以下类别中选择：
科技、AI、iOS/移动开发、GIS/地图/定位、校园、社会、娱乐、游戏、国际、财经、网文/内容创作、其他。

热点信息：
标题：{event_data.get('title', '未知')}
正文/内容：{event_data.get('rawHeat', '暂无详细内容')}
来源平台：{event_data.get('platform', '未知')}
来源链接：{event_data.get('url', '无')}

输出 JSON 格式要求包含以下字段：
{{
  "summary": "100字内摘要",
  "category": "所属分类",
  "tags": ["标签1", "标签2"],
  "credibility": "可信度等级",
  "riskLevel": "低/中/高",
  "creativeValue": 8,
  "angles": ["角度1", "角度2", "角度3"],
  "suggestion": "跟进建议"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一个严格输出 JSON 的热点分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            # 解析 JSON
            analysis_result = json.loads(content)
            
            # 将分析结果合并到原始数据中返回
            result = event_data.copy()
            result.update(analysis_result)
            return result
            
        except Exception as e:
            print(f"Agent 分析失败: {e}")
            return event_data

if __name__ == "__main__":
    agent = AnalyzerAgent()
    test_event = {
        "title": "OpenAI 发布新的 O3 模型引发广泛讨论",
        "platform": "百度热搜",
        "url": "https://top.baidu.com"
    }
    print("开始分析测试数据...")
    result = agent.analyze_event(test_event)
    print(json.dumps(result, ensure_ascii=False, indent=2))
