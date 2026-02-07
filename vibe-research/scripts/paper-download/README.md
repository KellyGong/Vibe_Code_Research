<h1 align="center">📥 Paper Download Scripts</h1>

<p align="center">
  <b>Multi-source paper acquisition with cascading retry</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Nature-Cookie_Auth-4CAF50" alt="Nature"/>
  <img src="https://img.shields.io/badge/arXiv-Direct-B31B1B" alt="arXiv"/>
  <img src="https://img.shields.io/badge/Semantic_Scholar-API-1976D2" alt="S2"/>
  <img src="https://img.shields.io/badge/Unpaywall-Open_Access-yellow" alt="Unpaywall"/>
  <img src="https://img.shields.io/badge/PMC-PubMed_Central-blue" alt="PMC"/>
</p>

---

<details open>
<summary><b>🇺🇸 English</b></summary>

## Overview

Three scripts that work together as a **download cascade**:

```
download_nature.py  →  download_missing.py  →  download_retry.py
     Nature PDFs         Other sources           Retry failed ones
```

### Prerequisites

```bash
pip install requests pandas tqdm
```

---

### 1. `download_nature.py` — Nature Journal Downloader

Downloads papers from Nature journals using browser cookie authentication.

```bash
python download_nature.py --csv papers.csv --output ./nature_pdfs --cookies cookies.json
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--csv` | CSV file with paper URLs **(required)** | — |
| `--output` | Output directory | `./nature_pdfs` |
| `--cookies` | Cookie JSON file | `./cookies.json` |

**Cookie Setup:**

1. Install **Cookie-Editor** Chrome extension
2. Visit `https://www.nature.com` and log in with your institution
3. Click Cookie-Editor → **Export as JSON**
4. Save the exported content to `cookies.json`

**Features:**
- Auto-detects Nature article URLs from CSV
- Validates downloaded PDFs (checks Content-Type + file header)
- Tracks progress with `downloaded.txt` / `failed.txt`
- Retries up to 3 times per paper

---

### 2. `download_missing.py` — Multi-source Downloader

Downloads non-Nature papers from multiple sources with multi-threading.

```bash
python download_missing.py --csv papers.csv --output ./downloads --proxy http://127.0.0.1:7890
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--csv` | CSV file with paper info **(required)** | — |
| `--output` | Output directory | `./downloads` |
| `--proxy` | HTTP proxy URL | _(none)_ |

**Download Strategy (in order):**
1. Direct PDF link
2. arXiv ID extraction → PDF
3. Semantic Scholar API → OpenAccess PDF
4. DOI-based URL conversion

**Features:**
- 8 parallel download threads
- Auto venue abbreviation (NeurIPS, ICML, ACL, ...)
- Skips already-downloaded files
- Saves failures to `download_failed.txt`

---

### 3. `download_retry.py` — Retry with Alternative Sources

Retries failed downloads using academic open-access APIs.

```bash
python download_retry.py --failed-file download_failed.txt --output ./downloads --proxy http://127.0.0.1:7890
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--failed-file` | Failed papers list **(required)** | — |
| `--output` | Output directory | `./downloads` |
| `--proxy` | HTTP proxy URL | _(none)_ |

**Sources:**
- **arXiv API** — title-based search
- **Unpaywall** — via Crossref DOI lookup
- **PubMed Central** — open access repository

**Features:**
- 4 parallel threads
- Validates file size (minimum 5KB)
- Outputs remaining failures to `download_still_failed.txt`

</details>

---

<details>
<summary><b>🇨🇳 中文</b></summary>

## 概述

三个脚本组成 **级联下载流水线**：

```
download_nature.py  →  download_missing.py  →  download_retry.py
    Nature 论文           其他来源论文            重试失败的论文
```

### 安装依赖

```bash
pip install requests pandas tqdm
```

---

### 1. `download_nature.py` — Nature 期刊下载器

使用浏览器 Cookie 认证下载 Nature 系列论文。

```bash
python download_nature.py --csv papers.csv --output ./nature_pdfs --cookies cookies.json
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--csv` | 包含论文URL的CSV文件 **（必填）** | — |
| `--output` | 输出目录 | `./nature_pdfs` |
| `--cookies` | Cookie JSON 文件 | `./cookies.json` |

**Cookie 获取方法：**

1. 安装 Chrome 扩展 **Cookie-Editor**
2. 访问 `https://www.nature.com` 并通过机构登录
3. 点击 Cookie-Editor → **Export as JSON**
4. 将导出内容保存为 `cookies.json`

**特性：**
- 自动从CSV中识别 Nature 文章 URL
- 验证下载的PDF（检查 Content-Type + 文件头）
- 用 `downloaded.txt` / `failed.txt` 追踪进度
- 每篇论文最多重试3次

---

### 2. `download_missing.py` — 多源下载器

多线程从多个来源下载非 Nature 论文。

```bash
python download_missing.py --csv papers.csv --output ./downloads --proxy http://127.0.0.1:7890
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--csv` | 论文信息CSV文件 **（必填）** | — |
| `--output` | 输出目录 | `./downloads` |
| `--proxy` | HTTP代理地址 | _(无)_ |

**下载策略（按优先级）：**
1. 直接 PDF 链接
2. 提取 arXiv ID → 下载 PDF
3. Semantic Scholar API → OpenAccess PDF
4. DOI 链接转换

**特性：**
- 8 线程并行下载
- 自动识别会议/期刊缩写（NeurIPS, ICML, ACL...）
- 跳过已下载文件
- 失败记录保存至 `download_failed.txt`

---

### 3. `download_retry.py` — 多源重试下载

使用学术开放获取 API 重试下载失败的论文。

```bash
python download_retry.py --failed-file download_failed.txt --output ./downloads --proxy http://127.0.0.1:7890
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--failed-file` | 失败论文列表 **（必填）** | — |
| `--output` | 输出目录 | `./downloads` |
| `--proxy` | HTTP代理地址 | _(无)_ |

**数据源：**
- **arXiv API** — 按标题搜索
- **Unpaywall** — 通过 Crossref 获取 DOI 后查询
- **PubMed Central** — 开放获取资源库

**特性：**
- 4 线程并行
- 验证文件大小（最小 5KB）
- 仍失败的记录保存至 `download_still_failed.txt`

</details>
