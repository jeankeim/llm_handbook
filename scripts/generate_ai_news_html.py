#!/usr/bin/env python3
"""
AI技术动态页面自动生成脚本
根据JSON数据动态生成ai-tech-news.html
支持按月份分组的时间线布局
"""

import json
import os
from datetime import datetime

# 月份颜色配置
MONTH_COLORS = {
    "2026-03": {"bg": "red-600", "light": "red-50", "border": "red-100", "text": "red-800"},
    "2026-02": {"bg": "indigo-600", "light": "indigo-50", "border": "indigo-100", "text": "indigo-800"},
    "2026-01": {"bg": "blue-600", "light": "blue-50", "border": "blue-100", "text": "blue-800"},
}

# 分类颜色映射
CATEGORY_COLORS = {
    "市场格局": "red",
    "国产登顶": "purple",
    "模型发布": "green",
    "开源模型": "orange",
    "视频生成": "pink",
    "海外动态": "blue",
    "工具框架": "teal",
    "应用落地": "cyan",
    "最新动态": "gray"
}


def load_news_data():
    """加载新闻数据"""
    data_file = "data/ai-news.json"
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def get_month_display(month_key):
    """获取月份显示名称"""
    month_map = {
        "2026-03": "3月",
        "2026-02": "2月", 
        "2026-01": "1月"
    }
    return month_map.get(month_key, month_key)


def format_date(date_str):
    """格式化日期显示"""
    try:
        # 尝试解析日期
        for fmt in ["%Y-%m-%d", "%a, %d %b %Y %H:%M:%S %z"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%m-%d")
            except:
                continue
    except:
        pass
    # 返回简化格式
    if "-" in date_str:
        parts = date_str.split("-")
        if len(parts) >= 3:
            return f"{parts[1]}-{parts[2]}"
    return date_str


def generate_hot_news_by_month(months_data):
    """生成按月份分组的热点新闻HTML"""
    if not months_data:
        return ""
    
    # 按月份倒序排列
    sorted_months = sorted(months_data.keys(), reverse=True)
    
    html = ""
    
    for month_key in sorted_months:
        month_data = months_data[month_key]
        colors = MONTH_COLORS.get(month_key, MONTH_COLORS["2026-03"])
        month_display = get_month_display(month_key)
        
        html += f'''            <!-- ===== {month_key}：{month_data.get("theme", "")} ===== -->
            <div class="mb-10">
                <div class="flex items-center mb-6">
                    <div class="w-12 h-12 bg-{colors["bg"]} text-white rounded-full flex items-center justify-center font-bold text-lg mr-4">{month_display}</div>
                    <div>
                        <h3 class="text-xl font-bold text-gray-900">{month_data.get("theme", "")}</h3>
                        <p class="text-sm text-gray-500">{month_data.get("description", "")}</p>
                    </div>
                </div>
                <div class="grid md:grid-cols-2 gap-6">
'''
        
        # 获取该月的新闻
        news_list = month_data.get("news", [])[:6]  # 最多6条
        
        for news in news_list:
            category = news.get("category", "最新动态")
            color = CATEGORY_COLORS.get(category, "gray")
            date_display = format_date(news.get("date", ""))
            
            html += f'''                    <div class="news-card bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
                        <div class="flex items-center justify-between mb-4">
                            <span class="px-3 py-1 bg-{color}-100 text-{color}-700 rounded-full text-xs font-semibold">{category}</span>
                            <span class="text-gray-400 text-sm">{date_display}</span>
                        </div>
                        <h3 class="text-xl font-semibold mb-2 text-gray-900">{news["title"]}</h3>
                        <p class="text-gray-600 text-sm mb-4">{news.get("summary", "")}</p>
                        <div class="flex flex-wrap items-center text-sm text-gray-500 gap-2">
'''
            # 添加标签
            for tag in news.get("tags", [])[:3]:
                html += f'                            <span class="px-2 py-1 bg-gray-100 rounded">🏷️ {tag}</span>\n'
            
            html += '''                        </div>
                    </div>
'''
        
        html += '''                </div>
            </div>

'''
    
    return html


def generate_timeline_by_month(months_data):
    """生成按月份分组的模型发布时间线HTML"""
    if not months_data:
        return ""
    
    sorted_months = sorted(months_data.keys(), reverse=True)
    
    html = '''                <!-- Timeline Items - 按时间倒序排列 -->
                <div class="space-y-8">
'''
    
    for month_key in sorted_months:
        month_data = months_data[month_key]
        colors = MONTH_COLORS.get(month_key, MONTH_COLORS["2026-03"])
        month_display = get_month_display(month_key)
        
        html += f'''
                    <!-- ===== {month_key} ===== -->
                    <div class="relative flex items-start">
                        <div class="absolute left-0 w-12 h-12 bg-{colors["bg"]} text-white rounded-full flex items-center justify-center font-bold z-10">{month_display}</div>
                        <div class="ml-16 flex-1">
                            <h3 class="text-lg font-bold text-gray-900 mb-4">{month_key} · {month_data.get("theme", "")}</h3>
                            <div class="space-y-4">
'''
        
        # 获取该月的模型发布新闻
        news_list = month_data.get("news", [])
        
        for news in news_list:
            date_display = format_date(news.get("date", ""))
            
            html += f'''                                <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
                                    <div class="flex items-center justify-between mb-2">
                                        <h4 class="font-semibold">{news["title"]}</h4>
                                        <span class="text-sm text-gray-400">{date_display}</span>
                                    </div>
                                    <p class="text-gray-600 text-sm">{news.get("summary", "")}</p>
                                </div>
'''
        
        html += '''                            </div>
                        </div>
                    </div>
'''
    
    html += '''
                </div>
'''
    return html


def generate_tech_trends_section(tech_trends):
    """生成技术趋势HTML片段"""
    if not tech_trends:
        return ""
    
    html = '<div class="grid md:grid-cols-3 gap-6">\n'
    
    icon_colors = {
        "🧠": "indigo",
        "🎬": "purple",
        "⚡": "blue",
        "🔒": "green",
        "🏢": "orange",
        "🤖": "red",
        "🇨🇳": "red",
        "📱": "pink",
        "🔓": "teal"
    }
    
    for trend in tech_trends:
        icon = trend.get("icon", "📊")
        color = icon_colors.get(icon, "gray")
        
        html += f'''                <!-- Trend: {trend["title"]} -->
                <div class="bg-gradient-to-br from-{color}-50 to-{color}-100 rounded-xl p-6 border border-{color}-100">
                    <div class="w-12 h-12 bg-{color}-600 text-white rounded-lg flex items-center justify-center text-2xl mb-4">{icon}</div>
                    <h3 class="text-lg font-semibold mb-2">{trend["title"]}</h3>
                    <p class="text-gray-600 text-sm">{trend["description"]}</p>
                </div>
'''
    
    html += '            </div>'
    return html

def generate_tools_section(tool_updates):
    """生成工具框架HTML片段"""
    if not tool_updates:
        return ""
    
    html = '''            <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
                <table class="w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">工具/框架</th>
                            <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">最新版本</th>
                            <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">主要更新</th>
                            <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">发布时间</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
'''
    
    for tool in tool_updates:
        html += f'''                        <tr class="hover:bg-gray-50">
                            <td class="px-6 py-4 font-medium">{tool["name"]}</td>
                            <td class="px-6 py-4"><span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">{tool["version"]}</span></td>
                            <td class="px-6 py-4 text-sm text-gray-600">{tool["update"]}</td>
                            <td class="px-6 py-4 text-sm text-gray-400">{tool["date"]}</td>
                        </tr>
'''
    
    html += '''                    </tbody>
                </table>
            </div>'''
    return html

def generate_tools_by_month(tool_updates):
    """生成按月份分组的工具与框架更新HTML"""
    if not tool_updates:
        return ""
    
    html = '<!-- 按时间线分组的工具与框架更新 -->\n            <div class="space-y-8">\n'
    
    # 按月份倒序
    sorted_months = sorted(tool_updates.keys(), reverse=True)
    
    for month_key in sorted_months:
        month_tools = tool_updates[month_key]
        colors = MONTH_COLORS.get(month_key, MONTH_COLORS["2026-03"])
        
        # 根据月份确定主题描述
        theme_desc = {
            "2026-03": "智能体应用与开发工具升级",
            "2026-02": "基础设施与开发框架更新",
            "2026-01": "年初工具链优化"
        }.get(month_key, "工具与框架更新")
        
        html += f'''
                <!-- {month_key} -->
                <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
                    <div class="bg-{colors["light"]} px-6 py-3 border-b border-{colors["border"]}">
                        <h3 class="font-bold text-{colors["text"]}">{month_key} · {theme_desc}</h3>
                    </div>
                    <table class="w-full">
                        <tbody class="divide-y divide-gray-100">
'''
        
        for tool in month_tools:
            html += f'''                            <tr class="hover:bg-gray-50">
                                <td class="px-6 py-4 font-medium w-1/5">{tool["name"]}</td>
                                <td class="px-6 py-4 w-1/6"><span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">{tool["version"]}</span></td>
                                <td class="px-6 py-4 text-sm text-gray-600">{tool["update"]}</td>
                            </tr>
'''
        
        html += '''                        </tbody>
                    </table>
                </div>
'''
    
    html += '''
            </div>'''
    return html


def generate_full_html(data):
    """生成完整的HTML页面"""
    
    # 获取月份数据
    months_data = data.get("months", {})
    
    # 生成各个板块内容（使用新的月份分组函数）
    hot_news_html = generate_hot_news_by_month(months_data)
    timeline_html = generate_timeline_by_month(months_data)
    trends_html = generate_tech_trends_section(data.get("techTrends", []))
    tools_html = generate_tools_by_month(data.get("toolUpdates", {}))
    
    # 获取最后更新时间
    last_updated = data.get("lastUpdated", datetime.now().strftime("%Y-%m-%d"))
    
    # HTML模板
    template_str = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>最新AI技术发展汇总 - LLM Handbook</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .news-card {
            transition: all 0.3s ease;
        }
        .news-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }
        .tag-new {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .timeline-line {
            position: absolute;
            left: 24px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(to bottom, #667eea, #764ba2);
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-md border-b border-gray-200 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <a href="index.html" class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">LLM Handbook</a>
                    <span class="mx-3 text-gray-300">|</span>
                    <span class="text-gray-600">AI技术动态</span>
                </div>
                <div class="hidden md:flex space-x-6">
                    <a href="index.html" class="text-gray-600 hover:text-indigo-600">返回手册</a>
                    <a href="#latest" class="text-gray-600 hover:text-indigo-600">最新动态</a>
                    <a href="#models" class="text-gray-600 hover:text-indigo-600">模型发布</a>
                    <a href="#trends" class="text-gray-600 hover:text-indigo-600">技术趋势</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-32 pb-16 bg-gradient-to-br from-indigo-50 via-white to-purple-50">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <div class="inline-flex items-center px-4 py-2 bg-indigo-100 text-indigo-700 rounded-full text-sm mb-6">
                <span class="w-2 h-2 bg-indigo-600 rounded-full mr-2 animate-pulse"></span>
                实时更新
            </div>
            <h1 class="text-4xl md:text-5xl font-bold mb-6">
                最新AI技术<br>
                <span class="gradient-text">发展汇总</span>
            </h1>
            <p class="text-xl text-gray-600 mb-8">追踪大模型领域最新动态 · 把握技术发展趋势</p>
            <div class="flex justify-center gap-4 text-sm">
                <span class="px-4 py-2 bg-white rounded-lg shadow-sm">
                    <strong class="text-indigo-600">2026年</strong> 持续更新
                </span>
                <span class="px-4 py-2 bg-white rounded-lg shadow-sm">
                    <strong class="text-purple-600">覆盖</strong> 模型/工具/应用
                </span>
            </div>
        </div>
    </section>

    <!-- Latest News Section -->
    <section id="latest" class="py-16 bg-white">
        <div class="max-w-5xl mx-auto px-4">
            <div class="flex items-center mb-8">
                <span class="w-10 h-10 bg-red-100 text-red-600 rounded-lg flex items-center justify-center font-bold mr-3">🔥</span>
                <h2 class="text-3xl font-bold">最新热点</h2>
                <span class="ml-4 px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm tag-new">AUTO</span>
            </div>
            
''' + hot_news_html + '''
        </div>
    </section>

    <!-- Model Releases Timeline -->
    <section id="models" class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4">
            <div class="flex items-center mb-8">
                <span class="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center font-bold mr-3">🚀</span>
                <h2 class="text-3xl font-bold">模型发布时间线</h2>
            </div>

            <div class="relative">
                <div class="timeline-line"></div>
                
''' + timeline_html + '''
            </div>
        </div>
    </section>

    <!-- Tech Trends Section -->
    <section id="trends" class="py-16 bg-white">
        <div class="max-w-5xl mx-auto px-4">
            <div class="flex items-center mb-8">
                <span class="w-10 h-10 bg-purple-100 text-purple-600 rounded-lg flex items-center justify-center font-bold mr-3">📈</span>
                <h2 class="text-3xl font-bold">技术趋势洞察</h2>
            </div>

''' + trends_html + '''
        </div>
    </section>

    <!-- Tools & Frameworks -->
    <section class="py-16 bg-gray-50">
        <div class="max-w-5xl mx-auto px-4">
            <div class="flex items-center mb-8">
                <span class="w-10 h-10 bg-teal-100 text-teal-600 rounded-lg flex items-center justify-center font-bold mr-3">🛠️</span>
                <h2 class="text-3xl font-bold">工具与框架更新</h2>
            </div>

''' + tools_html + '''
        </div>
    </section>

    <!-- Subscribe Section -->
    <section class="py-16 bg-white">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <div class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 md:p-12 text-white">
                <h2 class="text-2xl md:text-3xl font-bold mb-4">持续追踪AI技术发展</h2>
                <p class="text-indigo-100 mb-8">本页面定期更新最新的大模型技术动态、模型发布和行业趋势</p>
                <div class="flex flex-col sm:flex-row justify-center gap-4">
                    <a href="index.html" class="px-8 py-3 bg-white text-indigo-600 rounded-lg font-semibold hover:bg-gray-100 transition">
                        返回手册首页
                    </a>
                    <a href="https://github.com/jeankeim/aidata" target="_blank" class="px-8 py-3 bg-indigo-700 text-white rounded-lg font-semibold hover:bg-indigo-800 transition">
                        查看GitHub仓库
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 bg-gray-50 border-t border-gray-200">
        <div class="max-w-5xl mx-auto px-4 text-center text-gray-500 text-sm">
            <p>最后更新：''' + last_updated + ''' | 数据来源：官方发布、技术社区、行业报告</p>
            <p class="mt-2">© 2026 LLM Handbook. MIT License.</p>
            <p class="mt-2 text-xs text-gray-400">💡 提示：本页面由AI自动更新，每週一自动抓取最新资讯。AI竞赛已进入新的加速阶段，保持关注和学习已是"必选项"。</p>
        </div>
    </footer>
</body>
</html>'''

    return template_str

def main():
    """主函数"""
    print("开始生成AI技术动态页面...")
    
    # 加载数据
    data = load_news_data()
    if not data:
        print("❌ 未找到数据文件 data/ai-news.json")
        return False
    
    # 生成HTML
    html_content = generate_full_html(data)
    
    # 写入文件
    output_file = "ai-tech-news.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 页面已生成: {output_file}")
    print(f"📊 数据统计:")
    
    # 统计月份数据
    months_data = data.get("months", {})
    total_news = sum(len(m.get("news", [])) for m in months_data.values())
    print(f"   - 月份分组: {len(months_data)} 个")
    print(f"   - 新闻总数: {total_news} 条")
    for month_key, month_data in sorted(months_data.items(), reverse=True):
        print(f"     · {month_key}: {len(month_data.get('news', []))} 条")
    
    print(f"   - 技术趋势: {len(data.get('techTrends', []))} 项")
    print(f"   - 工具更新: {sum(len(tools) for tools in data.get('toolUpdates', {}).values())} 个")
    print(f"⏰ 最后更新: {data.get('lastUpdated', '未知')}")
    
    return True

if __name__ == "__main__":
    main()