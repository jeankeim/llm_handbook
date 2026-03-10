# 🤖 AI技术动态自动化更新系统

## 📋 系统概述

本系统实现了 `ai-tech-news.html` 页面的**全自动更新**，无需人工干预即可保持内容最新。

## 🏗️ 系统架构

```
┌─────────────────┐    每周一9:00 UTC    ┌─────────────────────┐
│   GitHub Actions │ ──────────────────▶ │ update_ai_news.py   │
│   (定时触发)     │                     │ (RSS数据抓取)       │
└─────────────────┘                     └─────────────────────┘
                                                │
                                                ▼
                                        ┌─────────────────────┐
                                        │ data/ai-news.json   │
                                        │ (结构化数据存储)    │
                                        └─────────────────────┘
                                                │
                                                ▼
                                        ┌─────────────────────┐
                                        │ generate_ai_news_   │
                                        │ html.py             │
                                        │ (HTML自动生成)      │
                                        └─────────────────────┘
                                                │
                                                ▼
                                        ┌─────────────────────┐
                                        │ ai-tech-news.html   │
                                        │ (最终展示页面)      │
                                        └─────────────────────┘
                                                │
                                                ▼
                                        ┌─────────────────────┐
                                        │ GitHub PR (人工审核)│
                                        └─────────────────────┘
```

## 📁 文件结构

```
llm-handbook/
├── .github/
│   └── workflows/
│       └── update-ai-news.yml          # GitHub Actions工作流
├── scripts/
│   ├── update_ai_news.py              # RSS数据抓取脚本
│   └── generate_ai_news_html.py       # HTML页面生成脚本
├── data/
│   └── ai-news.json                   # 结构化数据文件
├── docs/
│   └── AI_AUTO_UPDATE_SYSTEM.md       # 本说明文档
└── ai-tech-news.html                  # 自动生成的目标页面
```

## 🔧 核心组件详解

### 1. GitHub Actions 工作流 (`update-ai-news.yml`)

**触发条件：**
- ⏰ **定时触发**：每周一 UTC 时间 9:00
- 🖱️ **手动触发**：通过 GitHub 界面随时运行

**执行流程：**
1. 检出代码仓库
2. 设置 Python 环境
3. 安装依赖包 (`feedparser`, `requests`, `jinja2`)
4. 运行数据抓取脚本
5. 运行HTML生成脚本
6. 检查是否有变更
7. 如有变更，自动创建 Pull Request

### 2. 数据抓取脚本 (`update_ai_news.py`)

**功能：**
- 📡 从多个RSS源抓取AI相关新闻
- 🔍 关键词过滤，只保留相关性强的内容
- 💾 将结构化数据保存到JSON文件

**RSS源列表：**
```python
RSS_SOURCES = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/rss.xml", 
    "Google AI": "https://ai.googleblog.com/feeds/posts/default",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
}
```

**关键词过滤：**
```python
KEYWORDS = [
    "GPT", "Claude", "Gemini", "LLM", "大模型", "AI", "模型",
    "LangChain", "LlamaIndex", "RAG", "Agent", "多模态",
    "DeepSeek", "文心一言", "通义千问"
]
```

### 3. HTML生成脚本 (`generate_ai_news_html.py`)

**功能：**
- 📄 读取JSON数据文件
- 🎨 使用Jinja2模板引擎生成完整HTML
- 🔄 动态填充各个板块内容
- 💾 输出到 `ai-tech-news.html`

**生成的板块：**
- 🔥 最新热点（热点新闻卡片）
- 🚀 模型发布时间线
- 📈 技术趋势洞察
- 🛠️ 工具与框架更新

### 4. 数据存储 (`data/ai-news.json`)

**数据结构：**
```json
{
  "lastUpdated": "2026-03-09",
  "version": "1.0",
  "hotNews": [...],        // 热点新闻数组
  "modelTimeline": [...],  // 模型时间线
  "techTrends": [...],     // 技术趋势
  "toolUpdates": [...]     // 工具更新
}
```

## ⚙️ 配置说明

### 自定义更新频率

修改 `.github/workflows/update-ai-news.yml` 中的cron表达式：

```yaml
# 每周一9点UTC
schedule:
  - cron: '0 9 * * 1'

# 其他常用配置：
# 每天凌晨2点：'0 2 * * *'
# 每周三下午3点：'0 15 * * 3'  
# 每月1号上午10点：'0 10 1 * *'
```

### 添加新的RSS源

在 `scripts/update_ai_news.py` 中添加：

```python
RSS_SOURCES = {
    # ... 现有源
    "新平台名称": "https://example.com/rss.xml",
}
```

### 调整关键词过滤

在 `scripts/update_ai_news.py` 中修改：

```python
KEYWORDS = [
    # ... 现有关键词
    "新关键词1", "新关键词2"
]
```

## 🚀 使用方法

### 1. 手动触发更新

访问 GitHub 仓库页面：
```
https://github.com/your-username/your-repo/actions
```
找到 "Update AI News" 工作流，点击 "Run workflow"

### 2. 本地测试

```bash
# 安装依赖
pip install feedparser requests jinja2

# 运行数据抓取
python scripts/update_ai_news.py

# 生成HTML页面
python scripts/generate_ai_news_html.py
```

### 3. 查看更新历史

所有更新都会生成 Pull Request，可以在以下位置查看：
- GitHub PR 列表
- 提交历史记录
- `data/ai-news.json` 的 git blame

## 🔍 质量保证机制

### 1. 人工审核流程

每次自动更新都会创建 Pull Request，需要人工审核：

✅ **审核清单：**
- [ ] 新闻内容准确无误
- [ ] 日期格式正确  
- [ ] 来源链接可访问
- [ ] 无敏感或不当内容

### 2. 数据验证

脚本内置多种验证机制：
- URL可访问性检查
- 内容关键词匹配
- 数据格式校验
- 重复内容去重

### 3. 错误处理

- 网络异常自动重试
- 单个RSS源失败不影响整体
- 详细错误日志记录
- 失败时不会覆盖原有数据

## 📊 监控与维护

### 1. 查看运行状态

GitHub Actions 页面显示：
- ✅ 成功/失败状态
- 🕐 运行时间
- 📋 详细日志

### 2. 性能指标

可以通过以下方式监控：
- PR创建频率
- 数据更新及时性
- 页面访问量变化
- 用户反馈收集

### 3. 故障排除

常见问题及解决方案：

**问题：RSS源无法访问**
- 检查网络连接
- 验证RSS链接有效性
- 考虑更换备用源

**问题：关键词匹配过少**
- 扩展关键词列表
- 调整匹配策略
- 添加同义词处理

**问题：HTML生成失败**
- 检查模板语法
- 验证数据完整性
- 查看Python环境依赖

## 🔄 扩展功能

### 1. 多语言支持

可以扩展支持英文、日文等多语言版本。

### 2. 社交媒体集成

添加Twitter、微信公众号等内容源。

### 3. 邮件通知

更新成功后自动发送邮件通知。

### 4. 数据分析

统计访问数据、热门话题等分析功能。

## 📞 技术支持

如有问题，请：
1. 查看GitHub Actions运行日志
2. 检查 `data/ai-news.json` 内容
3. 验证本地环境依赖
4. 提交Issue或联系维护者

---
*最后更新：2026年3月9日*