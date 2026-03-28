#!/usr/bin/env python3
"""
AI新闻自动更新脚本
用于GitHub Actions定时抓取AI技术动态
支持按月份分组的数据结构
"""

import json
import os
import re
import ssl
from datetime import datetime
from urllib import request
from urllib.error import URLError

# 禁用SSL验证（某些RSS源可能需要）
ssl._create_default_https_context = ssl._create_unverified_context

# RSS源配置
RSS_SOURCES = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/rss.xml",
    "Google AI": "https://ai.googleblog.com/feeds/posts/default",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
}

# 关键词过滤
KEYWORDS = [
    "GPT", "Claude", "Gemini", "LLM", "大模型", "AI", "模型",
    "LangChain", "LlamaIndex", "RAG", "Agent", "多模态",
    "DeepSeek", "文心一言", "通义千问", "Kimi", "豆包", "Qwen"
]

# 月份主题配置
MONTH_THEMES = {
    "2026-03": {"theme": "全球化竞争与格局逆转", "desc": "国产模型调用量历史性反超，实时多模态交互成为新战场"},
    "2026-02": {"theme": "模型密集发布与性价比革命", "desc": "春节前后成为'兵家必争之地'，MoE架构带来成本大幅降低"},
    "2026-01": {"theme": "推理与多模态的年初攻势", "desc": "开年各大厂商展现极强进攻性，重点提升深度推理和多模态能力"},
}


def fetch_rss(url, source_name):
    """获取RSS内容"""
    try:
        req = request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except URLError as e:
        print(f"获取 {source_name} RSS失败: {e}")
        return None
    except Exception as e:
        print(f"解析 {source_name} 出错: {e}")
        return None


def parse_rss_content(xml_content, source_name):
    """解析RSS XML内容，提取新闻条目"""
    if not xml_content:
        return []
    
    news_items = []
    item_pattern = r'<item>(.*?)</item>'
    title_pattern = r'<title>(.*?)</title>'
    link_pattern = r'<link>(.*?)</link>'
    desc_pattern = r'<description>(.*?)</description>'
    date_pattern = r'<pubDate>(.*?)</pubDate>'
    
    items = re.findall(item_pattern, xml_content, re.DOTALL)
    
    for item in items[:5]:
        title_match = re.search(title_pattern, item)
        link_match = re.search(link_pattern, item)
        desc_match = re.search(desc_pattern, item)
        date_match = re.search(date_pattern, item)
        
        if title_match:
            title = title_match.group(1).strip()
            if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                news_items.append({
                    "title": title,
                    "link": link_match.group(1).strip() if link_match else "",
                    "description": desc_match.group(1).strip() if desc_match else "",
                    "date": date_match.group(1).strip() if date_match else "",
                    "source": source_name
                })
    
    return news_items


def categorize_news(title, description):
    """根据标题和描述分类新闻"""
    text = (title + " " + description).lower()
    
    categories = {
        "市场格局": ["调用量", "反超", "市场份额", "token", "出海"],
        "国产登顶": ["登顶", "榜首", "第一", "超越"],
        "模型发布": ["发布", "推出", "上线", "gpt", "claude", "gemini"],
        "开源模型": ["开源", "open source", "github"],
        "视频生成": ["视频", "video", "sora", "seedance"],
        "海外动态": ["google", "openai", "anthropic", "xai", "grok"],
    }
    
    for category, keywords in categories.items():
        if any(kw in text for kw in keywords):
            return category
    return "最新动态"


def extract_tags(title, description):
    """提取标签"""
    text = title + " " + description
    tags = []
    
    tag_keywords = {
        "百万上下文": ["百万", "1m", "上下文", "context"],
        "Token出海": ["出海", "openrouter"],
        "MoE架构": ["moe", "混合专家"],
        "Agent": ["agent", "智能体"],
        "多模态": ["多模态", "multimodal"],
        "性价比": ["成本", "价格", "性价比", "$/million"],
    }
    
    for tag, keywords in tag_keywords.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            tags.append(tag)
    
    return tags[:3]


def parse_date_to_month(date_str):
    """解析日期获取月份标识"""
    try:
        # 尝试多种日期格式
        for fmt in ["%Y-%m-%d", "%a, %d %b %Y %H:%M:%S %z", "%d %b %Y"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m")
            except:
                continue
    except:
        pass
    return datetime.now().strftime("%Y-%m")


def load_existing_data():
    """加载现有数据 - 新的月份分组结构"""
    data_file = "data/ai-news.json"
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "lastUpdated": "",
        "version": "2.0",
        "months": {},
        "techTrends": [],
        "toolUpdates": {}
    }


def save_data(data):
    """保存数据到JSON文件"""
    os.makedirs("data", exist_ok=True)
    with open("data/ai-news.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def organize_news_by_month(news_items):
    """按月份组织新闻"""
    months_data = {}
    
    for item in news_items:
        month_key = parse_date_to_month(item.get("date", ""))
        
        if month_key not in months_data:
            months_data[month_key] = {
                "month": month_key,
                "theme": MONTH_THEMES.get(month_key, {}).get("theme", "AI技术动态"),
                "description": MONTH_THEMES.get(month_key, {}).get("desc", ""),
                "news": []
            }
        
        news_entry = {
            "title": item["title"],
            "summary": item["description"][:150] + "..." if len(item["description"]) > 150 else item["description"],
            "date": item["date"],
            "category": categorize_news(item["title"], item["description"]),
            "tags": extract_tags(item["title"], item["description"]),
            "source": item["source"],
            "link": item["link"]
        }
        
        months_data[month_key]["news"].append(news_entry)
    
    return months_data


def main():
    """主函数"""
    print(f"开始更新AI新闻数据... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 加载现有数据
    data = load_existing_data()
    
    # 抓取RSS源
    all_news = []
    for source_name, rss_url in RSS_SOURCES.items():
        print(f"正在获取 {source_name}...")
        xml_content = fetch_rss(rss_url, source_name)
        if xml_content:
            news_items = parse_rss_content(xml_content, source_name)
            all_news.extend(news_items)
            print(f"  找到 {len(news_items)} 条相关新闻")
    
    # 更新数据
    if all_news:
        print(f"\n总共获取 {len(all_news)} 条新闻")
        
        # 按月份组织新闻
        months_data = organize_news_by_month(all_news)
        
        # 合并到现有数据
        for month_key, month_data in months_data.items():
            if month_key in data["months"]:
                # 合并新闻，去重
                existing_titles = {n["title"] for n in data["months"][month_key]["news"]}
                for news in month_data["news"]:
                    if news["title"] not in existing_titles:
                        data["months"][month_key]["news"].append(news)
            else:
                data["months"][month_key] = month_data
        
        # 更新最后更新时间
        data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
        
        # 保存数据
        save_data(data)
        print("数据已保存到 data/ai-news.json")
        print(f"按月份组织: {list(data['months'].keys())}")
    else:
        print("未获取到新数据")
    
    print("更新完成！")


if __name__ == "__main__":
    main()
