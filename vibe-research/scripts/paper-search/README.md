<h1 align="center">🔍 Paper Search Tool</h1>

<p align="center">
  <b>Multi-source literature search with AI translation</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Nature-Crawler-4CAF50" alt="Nature"/>
  <img src="https://img.shields.io/badge/Semantic_Scholar-API-1976D2" alt="S2"/>
  <img src="https://img.shields.io/badge/DeepSeek-Translation-8BC34A" alt="DeepSeek"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## What It Does

A beautiful Streamlit web application that **searches academic papers** from multiple sources in parallel, with built-in abstract translation.

### Key Features

| Feature | Description |
|---------|-------------|
| 🌐 **Multi-source search** | Nature journals (web scraping) + Semantic Scholar API |
| 🔄 **Parallel retrieval** | Concurrent requests with progress tracking |
| 🌍 **Abstract translation** | Batch Chinese translation via DeepSeek API |
| 🎯 **Smart filtering** | OR/AND keyword logic with strict local filtering |
| 📊 **Result management** | Deduplication, per-journal tabs, CSV export |
| 🎨 **Theme support** | Light / Dark / Glass UI themes |
| 🛡️ **Proxy support** | Clash API auto-rotation + manual proxy pool |

### Prerequisites

```bash
pip install streamlit requests pandas beautifulsoup4 openai pyyaml
```

### Configuration

```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

### Usage

```bash
streamlit run paper_search.py
```

The app opens at `http://localhost:8501` with two modes:

#### Mode 1: Online Search

1. **Configure journals** in the sidebar (Nature series + API journals)
2. **Enter keywords** — use `/` for OR, `;` for AND groups
   - Example: `Molecule/Molecular; Large Language Model/LLM`
3. **Set filters** — year range, citation lookup, strict filtering
4. **Click "Start Search"** — parallel retrieval begins
5. **Browse results** — per-journal tabs with card-style layout
6. **Export** — download as CSV

#### Mode 2: Result Analysis (Preview)

1. **Upload CSV** — supports merging 2 files
2. **Filter** — by journal, year, keywords
3. **Translate** — batch translate abstracts
4. **Export** — filtered results as CSV

### Proxy Setup (Optional)

For users behind firewalls:

| Method | Config |
|--------|--------|
| Clash API | Enter API URL + secret in sidebar |
| Manual proxy | Enter `http://127.0.0.1:7890` |
| Cookie auth | Paste Nature cookies for subscription content |

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 功能简介

一个美观的 Streamlit Web 应用，支持从多个数据源**并行检索学术论文**，内置摘要翻译功能。

### 核心特性

| 特性 | 说明 |
|------|------|
| 🌐 **多源检索** | Nature期刊（网页爬取）+ Semantic Scholar API |
| 🔄 **并行检索** | 多线程并发请求，实时进度展示 |
| 🌍 **摘要翻译** | 通过DeepSeek API批量翻译为中文 |
| 🎯 **智能过滤** | 支持 OR/AND 关键词逻辑 + 本地严格过滤 |
| 📊 **结果管理** | 自动去重、按期刊分Tab、CSV导出 |
| 🎨 **主题切换** | Light / Dark / Glass 三种UI主题 |
| 🛡️ **代理支持** | Clash API自动轮换 + 手动代理池 |

### 安装依赖

```bash
pip install streamlit requests pandas beautifulsoup4 openai pyyaml
```

### 配置

```bash
export DEEPSEEK_API_KEY="你的API密钥"
```

### 使用

```bash
streamlit run paper_search.py
```

应用在 `http://localhost:8501` 启动，包含两种模式：

#### 模式1：在线检索

1. **配置期刊** — 在侧边栏选择 Nature 系列 + API 期刊
2. **输入关键词** — 用 `/` 表示 OR，`;` 表示 AND
   - 示例：`Molecule/Molecular; Large Language Model/LLM`
3. **设置过滤** — 年份范围、引用查询、严格过滤
4. **点击「开始检索」** — 并行检索开始
5. **浏览结果** — 按期刊分Tab，卡片式展示
6. **导出** — 下载为 CSV

#### 模式2：结果分析 (Preview)

1. **上传 CSV** — 支持合并2个文件
2. **筛选** — 按期刊、年份、关键词过滤
3. **翻译** — 批量翻译摘要
4. **导出** — 筛选结果另存 CSV

### 代理设置（可选）

对于需要代理的用户：

| 方式 | 配置 |
|------|------|
| Clash API | 在侧边栏输入API地址 + Secret |
| 手动代理 | 输入 `http://127.0.0.1:7890` |
| Cookie认证 | 粘贴Nature Cookie用于订阅内容 |

</details>
