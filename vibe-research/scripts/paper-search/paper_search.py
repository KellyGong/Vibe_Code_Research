import os
import streamlit as st
import requests
import pandas as pd
import time
import random
import concurrent.futures
import urllib.parse
import json
import socket
import subprocess
import itertools
import uuid
import textwrap
from datetime import datetime
from bs4 import BeautifulSoup

# 新增：OpenAI SDK 用于调用 DeepSeek
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# 尝试导入 PyYAML
try:
    import yaml
except ImportError:
    yaml = None

# ================= 配置页面与自定义 CSS =================
st.set_page_config(
    page_title="DeepSearch Pro",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_CSS = """
<style>
:root {
  --primary: #ff5c5c;
  --primary-dark: #ff7a3d;
  --bg: #f6f8fb;
  --card: #ffffff;
  --card-blur: rgba(255,255,255,0.7);
  --text: #1f2a44;
  --muted: #6b7280;
  --border: #e5e7eb;
  --shadow: 0 12px 40px rgba(15,23,42,0.08);
}
.stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: radial-gradient(circle at 20% 20%, rgba(255,92,92,0.12), transparent 25%), radial-gradient(circle at 80% 0%, rgba(80,125,255,0.14), transparent 26%), var(--bg); }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(255,255,255,0.85), rgba(245,246,250,0.9)); backdrop-filter: blur(6px); }
.theme-card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 18px; box-shadow: var(--shadow); margin-bottom: 16px; }
.glass-card { background: var(--card-blur); border: 1px solid rgba(255,255,255,0.35); border-radius: 16px; padding: 18px; box-shadow: 0 15px 50px rgba(0,0,0,0.12); backdrop-filter: blur(12px); margin-bottom: 16px; }
.paper-card { border-radius: 14px; padding: 16px 18px; border: 1px solid rgba(226,232,240,0.8); box-shadow: 0 10px 32px rgba(15,23,42,0.08); background: var(--card); transition: transform .15s ease, box-shadow .2s ease; }
.paper-card:hover { transform: translateY(-2px); box-shadow: 0 16px 40px rgba(15,23,42,0.12); }
.badge { display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; color: white; margin-right: 6px; }
.badge-year { background: linear-gradient(135deg, #22c55e, #16a34a); }
.badge-journal { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.badge-cite { background: linear-gradient(135deg, #f59e0b, #f97316); }
.muted { color: var(--muted); font-size: 13px; }
.pill { display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border-radius:999px; background: rgba(255,92,92,0.08); color:#ff5c5c; font-weight:600; }
.metric-box { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 12px 14px; box-shadow: 0 6px 18px rgba(15,23,42,0.05); }
.hero { padding: 10px 16px 2px 16px; border-radius: 14px; background: linear-gradient(135deg, rgba(255,92,92,0.12), rgba(80,125,255,0.12)); border: 1px solid rgba(255,255,255,0.6); }
.stTabs [data-baseweb="tab"] { font-weight: 700; padding: 12px 14px; }
div.stButton > button { border-radius: 10px; font-weight: 700; padding: 0.6rem 0.9rem; }
</style>
"""

THEME_OVERRIDES = {
    "Light": "",
    "Dark": """
    <style>
    :root { --bg:#0f1115; --card:#151923; --card-blur:rgba(21,25,35,0.7); --text:#e5e7eb; --muted:#9ca3af; --border:#1f2937; --shadow:0 12px 40px rgba(0,0,0,0.35); }
    .stApp { background: radial-gradient(circle at 18% 20%, rgba(255,92,92,0.1), transparent 22%), radial-gradient(circle at 70% 0%, rgba(80,125,255,0.12), transparent 24%), var(--bg); color: var(--text); }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(21,25,35,0.95), rgba(21,25,35,0.85)); }
    </style>
    """,
    "Glass": """
    <style>
    :root { --bg: linear-gradient(135deg, #e9f0ff, #fef6ff); --card:#ffffffcc; --card-blur:rgba(255,255,255,0.65); --text:#14213d; --muted:#6b7280; --border:rgba(255,255,255,0.5); --shadow:0 18px 48px rgba(15,23,42,0.12); }
    .stApp { background: linear-gradient(120deg, rgba(255,255,255,0.7), rgba(233,240,255,0.9)); }
    section[data-testid="stSidebar"] { background: rgba(255,255,255,0.6); backdrop-filter: blur(14px); }
    </style>
    """
}

def apply_theme(name: str):
    """Inject base CSS + override without渲染成文本."""
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    override = THEME_OVERRIDES.get(name, "")
    if override:
        st.markdown(override, unsafe_allow_html=True)

# ================= DeepSeek 配置 =================
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

if OpenAI and DEEPSEEK_API_KEY:
    ds_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
else:
    ds_client = None

# ================= 常量配置 =================
NATURE_JOURNALS_MAP = {
    "Nature Machine Intelligence": "natmachintell",
    "Nature Computational Science": "natcomputsci",
    "Nature Communications": "ncomms",
    "Nature Methods": "nmeth",
    "Nature Chemistry": "nchem",
    "Nature": "nature",
    "Nature Biotechnology": "nbt",
    "Nature Biomedical Engineering": "natbiomedeng"
}

API_JOURNALS_LIST = [
    "IEEE Transactions on Pattern Analysis and Machine Intelligence", 
    "IEEE Transactions on Neural Networks and Learning Systems",      
    "IEEE Transactions on Knowledge and Data Engineering",
    "IEEE Transactions on Image Processing",
    "Science Advances",
    "Science",
    "NeurIPS",
    "ICLR",
    "ICML",
    "CVPR",
    "ICCV",
    "ECCV",
    "ACL",
    "Findings of the Association for Computational Linguistics",
    "EMNLP",
    "Findings of the Association for Computational Linguistics: EMNLP",
    "COLING",
    "NAACL",
    "AAAI",
    "IJCAI",
    "Bioinformatics",
    "ArXiv"
]

JOURNAL_DISPLAY_ABBR = {
    "Nature Machine Intelligence": "Nature MI",
    "Nature Computational Science": "Nature Comp. Sci",
    "Nature Communications": "Nature Comm",
    "Nature Methods": "Nature Methods",
    "Nature Chemistry": "Nature Chem",
    "IEEE Transactions on Pattern Analysis and Machine Intelligence": "IEEE TPAMI",
    "IEEE Transactions on Neural Networks and Learning Systems": "IEEE TNNLS",
    "IEEE Transactions on Knowledge and Data Engineering": "IEEE TKDE",
    "Science Advances": "Science Adv",
    "Association for Computational Linguistics": "ACL",
    "Findings of the Association for Computational Linguistics": "Findings of ACL",
    "Empirical Methods in Natural Language Processing": "EMNLP",
    "Findings of the Association for Computational Linguistics: EMNLP": "Findings of EMNLP",
    "International Conference on Computational Linguistics": "COLING",
    "North American Chapter of the Association for Computational Linguistics": "NAACL",
    "Association for the Advancement of Artificial Intelligence": "AAAI",
    "International Joint Conference on Artificial Intelligence": "IJCAI"
}

def deduplicate_dataframe(df):
    """Drop duplicates using a stable key of title + journal + year."""
    if df.empty: return df
    df = df.copy()
    title = df['Title'].fillna('').astype(str).str.strip().str.lower() if 'Title' in df else ""
    journal = df['Journal'].fillna('').astype(str).str.strip().str.lower() if 'Journal' in df else ""
    year = df['Year'].fillna('').astype(str) if 'Year' in df else ""
    df['_dedup_key'] = title + "|" + journal + "|" + year
    df = df.drop_duplicates(subset=['_dedup_key'])
    return df.drop(columns=['_dedup_key'])

def find_matched_terms(title_txt, abs_txt, filter_struct):
    """Return list of matched keywords (one per group) based on provided filter_struct."""
    if not filter_struct: return []
    content = (title_txt + " " + abs_txt).lower()
    matched = []
    for group in filter_struct:
        hit = None
        for k in group:
            clean_k = k.replace('"', '').replace("'", "").lower()
            if clean_k and clean_k in content:
                hit = clean_k
                break
        if hit: matched.append(hit)
    return matched

def item_key(obj, prefix="item"):
    """Create a stable key from a mapping-like row."""
    if obj is None: return prefix
    if isinstance(obj, dict):
        t = obj.get('Title')
        j = obj.get('Journal')
        y = obj.get('Year')
        u = obj.get('URL')
        k = obj.get('TranslateKey')
    else:
        t = obj['Title'] if 'Title' in obj else None
        j = obj['Journal'] if 'Journal' in obj else None
        y = obj['Year'] if 'Year' in obj else None
        u = obj['URL'] if 'URL' in obj else None
        k = obj['TranslateKey'] if 'TranslateKey' in obj else None
    if k: return str(k)
    return f"{prefix}_{hash(str(t))}_{hash(str(j))}_{hash(str(y))}_{hash(str(u))}"

def add_translate_key(df, prefix):
    """Add a stable translation key column for session translations."""
    df = df.copy()
    df['TranslateKey'] = [f"{prefix}_{idx}_{hash(str(title))}" for idx, title in zip(df.index, df['Title'])]
    return df

def apply_cn_column(df):
    """Populate Abstract_CN from existing column or session translations."""
    if df.empty: return df
    df = df.copy()
    def _get_cn(row):
        # existing CN value in CSV
        if 'Abstract_CN' in row and pd.notna(row['Abstract_CN']) and str(row['Abstract_CN']).strip():
            return row['Abstract_CN']
        key = row.get('TranslateKey')
        if key and key in st.session_state.get('translations', {}):
            return st.session_state['translations'][key]
        return None
    df['Abstract_CN'] = df.apply(_get_cn, axis=1)
    return df

def batch_translate(df, max_workers=1000):
    """Translate all abstracts missing CN and store into session + df column."""
    if df.empty or 'Abstract' not in df: return df, 0
    to_translate = []
    for idx, row in df.iterrows():
        key = row.get('TranslateKey')
        cn_val = row.get('Abstract_CN')
        abst = row.get('Abstract')
        if (not key) or (not abst) or str(abst).strip() in ["", "暂无摘要"]: 
            continue
        if cn_val and str(cn_val).strip(): 
            continue
        if key in st.session_state.get('translations', {}):
            continue
        to_translate.append((key, str(abst)))
    if not to_translate: 
        return df, 0
    workers = min(max_workers, len(to_translate))
    with st.spinner(f"批量翻译中... {len(to_translate)} 篇"):
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as exc:
            futures = {exc.submit(translate_text_deepseek, text): key for key, text in to_translate}
            for fut in concurrent.futures.as_completed(futures):
                res = fut.result()
                k = futures[fut]
                st.session_state['translations'][k] = res
    df = apply_cn_column(df)
    return df, len(to_translate)

# ================= 翻译逻辑 =================
def translate_text_deepseek(text):
    if not ds_client: return "请先安装 openai 库: pip install openai"
    if not text or len(text) < 10: return "摘要过短，无需翻译。"
    sys_prompt = "你是一位专业的学术论文翻译助手。请将用户的英文摘要翻译成通顺、准确的中文。保留专业术语的准确性。"
    try:
        response = ds_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": text}],
            stream=False, temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e: return f"翻译失败: {str(e)}"

# ================= Clash API 控制器 =================
class ClashAPI:
    def __init__(self, base_url="http://127.0.0.1:9090", secret=""):
        self.base_url = base_url.rstrip('/')
        self.secret = secret
        self.connected = False
    
    def _get_headers(self):
        headers = {}
        if self.secret: headers["Authorization"] = f"Bearer {self.secret}"
        return headers

    def _get_session(self):
        session = requests.Session()
        session.trust_env = False
        return session

    def test_connection(self):
        try:
            s = self._get_session()
            r = s.get(f"{self.base_url}/configs", headers=self._get_headers(), timeout=2)
            if r.status_code == 200:
                self.connected = True
                return True, "✅ 连接成功"
            elif r.status_code == 401: return False, "❌ 401 Unauthorized"
            else: return False, f"❌ HTTP {r.status_code}"
        except Exception as e: return False, f"❌ 无法连接: {str(e)}"

    def get_configs(self):
        try:
            s = self._get_session()
            r = s.get(f"{self.base_url}/configs", headers=self._get_headers(), timeout=2)
            return r.json() if r.status_code == 200 else {}
        except: return {}

    def patch_mode(self, mode):
        try:
            s = self._get_session()
            s.patch(f"{self.base_url}/configs", json={"mode": mode}, headers=self._get_headers(), timeout=2)
            return True
        except: return False
    
    def get_proxies(self):
        try:
            s = self._get_session()
            r = s.get(f"{self.base_url}/proxies", headers=self._get_headers(), timeout=2)
            return r.json()['proxies'] if r.status_code == 200 else {}
        except: return {}
        
    def select_proxy(self, group_name, proxy_name):
        try:
            s = self._get_session()
            safe_group = urllib.parse.quote(group_name)
            s.put(f"{self.base_url}/proxies/{safe_group}", json={"name": proxy_name}, headers=self._get_headers(), timeout=2)
            return True
        except: return False

if 'clash_api' not in st.session_state: st.session_state.clash_api = ClashAPI()

# ================= 代理池管理器 =================
class ProxyManager:
    def __init__(self): self.proxies = []
    def load_manual_proxies(self, text_input):
        if not text_input: return 0
        raw_list = text_input.replace('\n', ';').split(';')
        valid_proxies = []
        for p in raw_list:
            p = p.strip()
            if not p: continue
            if not p.startswith("http"): p = f"http://{p}"
            valid_proxies.append(p)
        self.proxies = valid_proxies
        return len(self.proxies)

if 'proxy_manager' not in st.session_state: st.session_state.proxy_manager = ProxyManager()

# ================= 浏览器伪装 =================
def get_browser_headers(manual_cookie=""):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.nature.com/",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1"
    }
    if manual_cookie: headers["Cookie"] = manual_cookie
    return headers

def test_proxy_connection(proxy_url):
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        start_t = time.time()
        r = requests.get("https://www.nature.com", proxies=proxies, timeout=10, headers=get_browser_headers())
        latency = (time.time() - start_t) * 1000
        if r.status_code == 200: return True, f"✅ 连接成功 ({latency:.0f}ms)"
        elif r.status_code in [303, 403]: return False, f"⚠️ 连通但被拦截 (Status {r.status_code})"
        else: return False, f"⚠️ Status {r.status_code}"
    except Exception as e: return False, f"❌ 连接失败: {str(e)}"

# ================= 辅助功能 =================
def fetch_google_scholar_citation(title, proxies):
    url = "https://scholar.google.com/scholar"
    params = {"q": title, "hl": "en", "as_sdt": "0,5"}
    try:
        time.sleep(random.uniform(1.0, 3.0))
        s = requests.Session()
        s.headers.update(get_browser_headers())
        r = s.get(url, params=params, proxies=proxies, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            res = soup.find("div", class_="gs_ri")
            if not res: return "0"
            for link in res.find_all("a"):
                txt = link.get_text()
                if "Cited by" in txt: return txt.replace("Cited by", "").strip()
                if "被引用次数" in txt: return txt.replace("被引用次数：", "").strip()
            return "0"
        elif r.status_code == 429: return "429(Busy)"
        return f"Err{r.status_code}"
    except: return "Error"

def fetch_nature_full_abstract(article_url, session):
    try:
        time.sleep(random.uniform(0.5, 1.5))
        r = session.get(article_url, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            abs_div = soup.find("div", id="Abs1-content")
            if abs_div: return abs_div.get_text(strip=True)
            sections = soup.find_all("div", class_="c-article-section__content")
            for sec in sections:
                t = sec.get_text(strip=True)
                if len(t) > 200: return t
            meta = soup.find("meta", attrs={"name": "description"})
            if meta: return meta.get("content", "").strip()
    except: pass
    return None

def switch_clash_node_worker(api_url, secret, group, nodes):
    try:
        if not nodes: return None
        target = random.choice(nodes)
        headers = {}
        if secret: headers["Authorization"] = f"Bearer {secret}"
        safe_group = urllib.parse.quote(group)
        requests.put(f"{api_url}/proxies/{safe_group}", json={"name": target}, headers=headers, timeout=1)
        return target
    except: return None

# ================= Nature Worker =================
def process_nature_article_enrichment(item, session, proxies, enable_full_abstract, enable_scholar, filter_kws_structured, strict_filter):
    logs = []
    if enable_full_abstract:
        full = fetch_nature_full_abstract(item['URL'], session)
        if full: 
            item['Abstract'] = full
            logs.append("Full Abs Fetched")
    
    if strict_filter and filter_kws_structured:
        content = (item['Title'] + " " + item['Abstract']).lower()
        is_match = True
        missing_groups = []
        for group in filter_kws_structured:
            group_match = False
            for k in group:
                clean_k = k.replace('"', '').replace("'", "").lower()
                if clean_k in content:
                    group_match = True
                    break
            if not group_match:
                is_match = False
                missing_groups.append(group)
                break 
        if not is_match:
            logs.append(f"Skipped")
            return None, logs

    if enable_scholar:
        cite = fetch_google_scholar_citation(item['Title'], proxies)
        item['Citations'] = cite
        logs.append(f"Scholar: {cite}")
        
    return item, logs

def scrape_nature_worker(task_args):
    q_str, j_name, j_code, start_y, end_y, use_proxy, proxies_list, cookie, clash_cfg, en_scholar, en_full_abs, filter_kws_struct, max_pages, strict_filter = task_args
    papers = []
    logs = []
    base_url = "https://www.nature.com/search"
    max_retries = 3 if use_proxy else 1
    
    for page_num in range(1, max_pages + 1):
        params = {"q": q_str, "journal": j_code, "order": "date_desc", "page": page_num}
        page_success = False
        for attempt in range(max_retries):
            switched = None
            if clash_cfg and clash_cfg.get('enabled') and clash_cfg.get('nodes'):
                switched = switch_clash_node_worker(clash_cfg['url'], clash_cfg['secret'], clash_cfg['group'], clash_cfg['nodes'])
                time.sleep(0.5)
            
            sess = requests.Session()
            sess.headers.update(get_browser_headers(cookie))
            proxies = None
            if use_proxy and proxies_list:
                p = proxies_list[0]
                proxies = {"http": p, "https": p}
            
            log_prefix = f"[{datetime.now().strftime('%H:%M:%S')}] {j_name} P{page_num} (Try {attempt+1})"
            if switched: logs.append(f"{log_prefix} | Switched: {switched}")
            
            try:
                resp = sess.get(base_url, params=params, proxies=proxies, timeout=15, allow_redirects=True)
                if "idp.nature.com" in resp.url or "authorize" in resp.url:
                    logs.append("  -> ⚠️ Blocked")
                    if attempt < max_retries-1: continue
                    break 
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    arts = soup.find_all("li", class_="app-article-list-row__item") or soup.find_all("article", class_="u-full-height")
                    if not arts:
                        logs.append("  -> No items.")
                        page_success = True 
                        break 
                    logs.append(f"  -> Found {len(arts)} items")
                    
                    prelim_papers = []
                    for art in arts:
                        try:
                            title_tag = art.find("a", class_="c-card__link")
                            if not title_tag: continue
                            title = title_tag.get_text().strip()
                            link = "https://www.nature.com" + title_tag['href'] if title_tag['href'].startswith("/") else title_tag['href']
                            date_tag = art.find("time")
                            py = 0
                            p_date = ""
                            if date_tag:
                                p_date = date_tag.get_text().strip()
                                if len(p_date) >= 4: py = int(p_date[-4:])
                            abs_txt = "暂无摘要"
                            sum_div = art.find("div", class_="c-card__summary")
                            if sum_div: abs_txt = sum_div.get_text().strip()
                            
                            if start_y <= py <= end_y:
                                prelim_papers.append({
                                    "Year": py, "DisplayDate": p_date, "Journal": JOURNAL_DISPLAY_ABBR.get(j_name, j_name),
                                    "FullJournal": j_name, "Title": title, "Citations": "N/A", "URL": link,
                                    "Abstract": abs_txt, "MatchKeyword": q_str, "Source": "Nature Official"
                                })
                        except: continue
                    
                    if prelim_papers:
                        # 内部并行处理详情
                        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exc:
                            futures = {exc.submit(process_nature_article_enrichment, p, sess, proxies, en_full_abs, en_scholar, filter_kws_struct, strict_filter): p for p in prelim_papers}
                            for fut in concurrent.futures.as_completed(futures):
                                try:
                                    p_res, p_logs = fut.result()
                                    if p_res: papers.append(p_res)
                                    if p_logs: logs.extend([f"    {l}" for l in p_logs])
                                except: pass
                    
                    page_success = True
                    break 
                if attempt < max_retries-1: continue
            except Exception as e:
                logs.append(f"  -> Err: {str(e)}")
                if attempt < max_retries-1: continue
        if not page_success: logs.append("  -> Page failed.")
            
    return papers, None, logs

# ================= API Worker =================
def search_api_worker(task_args):
    q_str, start, end, limit, venues_chunk, proxies, filter_kws_struct, strict_filter, ignore_venue_filter = task_args
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": q_str, "year": f"{start}-{end}", "limit": limit,
        "fields": "paperId,title,url,venue,year,abstract,citationCount,openAccessPdf,publicationDate"
    }
    if not ignore_venue_filter and venues_chunk:
        params["venue"] = ",".join(venues_chunk)
        
    logs = []
    max_retries = 3
    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(1.0, 3.0)) 
            r = requests.get(url, params=params, headers={"User-Agent": "ResearchTool/Pro"}, proxies=proxies, timeout=20)
            if r.status_code == 200:
                raw_data = r.json().get("data", [])
                filtered_data = []
                for p in raw_data:
                    if strict_filter and filter_kws_struct:
                        txt = (p.get("title","") + " " + (p.get("abstract") or "")).lower()
                        is_match = True
                        for group in filter_kws_struct:
                            group_match = False
                            for k in group:
                                clean_k = k.replace('"', '').replace("'", "").lower()
                                if clean_k in txt:
                                    group_match = True
                                    break
                            if not group_match:
                                is_match = False
                                break
                        if not is_match: continue
                    filtered_data.append(p)
                return filtered_data, None, logs
            elif r.status_code == 429:
                logs.append(f"⚠️ API 429 (Retry {attempt+1})")
                time.sleep(2 ** (attempt + 1))
                continue
            else:
                msg = f"Status {r.status_code}"
                logs.append(msg)
                return [], msg, logs
        except Exception as e:
            msg = str(e)
            logs.append(msg)
            if attempt < max_retries-1: 
                time.sleep(2)
                continue
            return [], msg, logs
    return [], "Max Retries", logs

def normalize_api_result(p, query_kw):
    """Map Semantic Scholar fields into the unified schema used by the UI."""
    venue_raw = p.get("venue")
    venue = str(venue_raw).strip() if venue_raw else "Unknown"
    pub_date = p.get("publicationDate") or ""
    display_date = pub_date.split("T")[0] if isinstance(pub_date, str) else ""
    year_val = p.get("year") or 0
    cite_val = p.get("citationCount")
    cite_val = cite_val if cite_val is not None else "N/A"
    
    open_pdf = p.get("openAccessPdf")
    pdf_url = open_pdf.get("url") if isinstance(open_pdf, dict) else None
    url_val = pdf_url or p.get("url") or None
    if (not url_val) and p.get("paperId"):
        url_val = f"https://www.semanticscholar.org/p/{p['paperId']}"
    url_val = str(url_val).strip() if url_val else None

    abs_txt = p.get("abstract") or "暂无摘要"
    title_txt = p.get("title") or "Untitled"

    return {
        "Year": year_val,
        "DisplayDate": display_date,
        "Journal": venue,
        "FullJournal": venue,
        "venue": venue,
        "Title": title_txt,
        "Citations": cite_val,
        "URL": url_val,
        "Abstract": abs_txt,
        "MatchKeyword": query_kw,
        "Source": "Semantic Scholar API",
        # Extra raw fields for reference
        "paperId": p.get("paperId"),
        "API_URL": p.get("url"),
        "OpenAccessPdf": open_pdf,
        "PublicationDate": pub_date
    }

# ================= 任务准备函数 =================
def prepare_nature_tasks(query_list, selected_map, start, end, use_proxy, proxies_list, cookie, clash_cfg, en_scholar, en_full_abs, filter_kws_struct, max_pages, strict_filter):
    tasks = []
    if clash_cfg and clash_cfg['nodes']:
        clash_cfg['nodes'] = [n for n in clash_cfg['nodes'] if 'DIRECT' not in n and 'REJECT' not in n]
    for q in query_list:
        if not q.strip(): continue
        for j_name, j_code in selected_map.items():
            tasks.append((q, j_name, j_code, start, end, use_proxy, proxies_list, cookie, clash_cfg, en_scholar, en_full_abs, filter_kws_struct, max_pages, strict_filter))
    return tasks

def prepare_api_tasks(query_list, start, end, limit, target_venues_list, use_proxy, proxies_list, filter_kws_struct, strict_filter, ignore_venue_filter):
    proxies = None
    if use_proxy and proxies_list:
        p = proxies_list[0]
        proxies = {"http": p, "https": p}
    tasks = []
    if ignore_venue_filter:
        for q in query_list:
            if not q.strip(): continue
            tasks.append((q, start, end, limit, None, proxies, filter_kws_struct, strict_filter, True))
    else:
        # Chunk size = 5 to reduce API calls
        chunk_size = 5
        venue_chunks = [target_venues_list[i:i + chunk_size] for i in range(0, len(target_venues_list), chunk_size)]
        for q in query_list:
            if not q.strip(): continue
            for chunk in venue_chunks:
                tasks.append((q, start, end, limit, chunk, proxies, filter_kws_struct, strict_filter, False))
    return tasks

# ================= UI =================
with st.sidebar:
    st.markdown("### 🎨 界面风格")
    ui_theme = st.radio("主题", ["Light", "Dark", "Glass"], index=["Light", "Dark", "Glass"].index(st.session_state.get("ui_theme", "Light")), horizontal=True)
    st.session_state["ui_theme"] = ui_theme
apply_theme(st.session_state["ui_theme"])

st.title("🔥 DeepSearch Pro")
st.caption("终极并行版 | Nature & Semantic Scholar | DeepSeek Translation")
app_mode = st.sidebar.selectbox("🎯 选择模式", ["🚀 在线检索", "📂 结果分析(Preview)"])

with st.container():
    total_cached = len(st.session_state.get('last_results', []) or [])
    st.markdown(f"""
    <div class="hero">
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="pill">并行 · 智能 · 可靠</div>
            <span class="muted">支持 Nature 爬取 + Semantic Scholar API + DeepSeek 翻译</span>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(160px,1fr)); gap:12px; margin-top:10px;">
            <div class="metric-box"><div class="muted">缓存结果</div><div style="font-size:24px; font-weight:800;">{total_cached}</div></div>
            <div class="metric-box"><div class="muted">年份范围</div><div style="font-size:24px; font-weight:800;">{2022} - {datetime.now().year+1}</div></div>
            <div class="metric-box"><div class="muted">翻译缓存</div><div style="font-size:24px; font-weight:800;">{len(st.session_state.get('translations', {}))}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if 'translations' not in st.session_state: st.session_state['translations'] = {}

# ================= 模式 1: 在线检索 =================
if app_mode == "🚀 在线检索":
    
    with st.sidebar:
        st.divider()
        with st.expander("📚 期刊配置", expanded=True):
            st.markdown("**Nature 系列**")
            sel_nat = st.multiselect("Nature Journals", list(NATURE_JOURNALS_MAP.keys()), 
                                     ["Nature Machine Intelligence", "Nature Computational Science", "Nature Communications"])
            sel_nat_map = {n: NATURE_JOURNALS_MAP[n] for n in sel_nat}
            
            st.markdown("**IEEE / Science / API**")
            ignore_venue_filter = st.checkbox("🌐 全库检索 (忽略期刊限制)", value=False)
            sel_api = st.multiselect("API Journals", API_JOURNALS_LIST, 
                                     ["Science Advances", "AAAI", "ACL", "Findings of the Association for Computational Linguistics", "EMNLP", "ArXiv"])

        with st.expander("🛠️ 网络与代理", expanded=False):
            user_cookie = st.text_area("Cookie (Nature)", placeholder="idp_session=...", height=60)
            clash_url = st.text_input("Clash API", "http://127.0.0.1:9090")
            clash_sec = st.text_input("Secret", "123456", type="password")
            api = st.session_state.clash_api
            api.base_url = clash_url.rstrip('/')
            api.secret = clash_sec
            
            if st.button("🔌 测试 Clash 连接"):
                ok, msg = api.test_connection()
                if ok: st.success(msg)
                else: st.error(msg)
                
            auto_rotate = st.checkbox("🔄 自动轮换 IP", value=False)
            rot_grp = "Proxy"
            avail_nodes = []
            if api.connected or api.test_connection()[0]:
                d = api.get_proxies()
                if d:
                    grps = [k for k, v in d.items() if v['type'] == 'Selector']
                    rot_grp = st.selectbox("轮换分组", grps, index=grps.index('Proxy') if 'Proxy' in grps else 0)
                    if rot_grp in d: avail_nodes = d[rot_grp]['all']

        with st.expander("📡 代理地址", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Load 7890"):
                    st.session_state.proxy_manager.load_manual_proxies("http://127.0.0.1:7890")
                    st.rerun()
            man_proxy = st.text_area("手动输入", value="http://127.0.0.1:7890", height=68, label_visibility="collapsed")
            if man_proxy: st.session_state.proxy_manager.load_manual_proxies(man_proxy)
            use_proxy = st.checkbox("🚀 开启代理", value=True)

        st.divider()
        st.markdown("**🔍 检索设置**")
        kw_in = st.text_area("关键词 (支持 '/' 表示 OR)", "Molecule/Molecular; Large Language Model/LLM", height=80, help="分号分隔不同组，组内用 / 分隔同义词。例如: A/B/C; D/E")
        s_mode = st.radio("逻辑", ["普通 (OR)", "高级 (AND)"], index=1, horizontal=True)
        
        strict_filter = st.checkbox("🔎 启用本地严格过滤", value=False)
        
        c1, c2 = st.columns(2)
        s_y = c1.number_input("年份起", 2022)
        e_y = c2.number_input("年份止", 2025)
        lim = st.slider("API Limit", 20, 100, 100)
        
        nat_pages = st.slider("Nature 爬取页数", 1, 5, 2)
        
        col_opt1, col_opt2 = st.columns(2)
        en_sch = col_opt1.checkbox("Scholar 引用", False)
        en_abs = col_opt2.checkbox("补全摘要", True)
        
        st.divider()
        run = st.button("🚀 开始检索", type="primary", use_container_width=True)

    if run:
        raw_kws = [k.strip() for k in kw_in.split(';') if k.strip()]
        if not raw_kws: st.warning("请输入关键词")
        else:
            results = []
            filter_kws_struct = []
            for k_grp in raw_kws:
                or_terms = [t.strip() for t in k_grp.split('/') if t.strip()]
                if or_terms: filter_kws_struct.append(or_terms)

            if "AND" in s_mode:
                nat_parts = []
                api_term_groups = []
                for group in filter_kws_struct:
                    group_terms_nat = []
                    for t in group:
                        if " " in t: group_terms_nat.append(f'"{t}"')
                        else: group_terms_nat.append(t)
                    if len(group_terms_nat) > 1: nat_parts.append("(" + " OR ".join(group_terms_nat) + ")")
                    else: nat_parts.append(group_terms_nat[0])
                    
                    group_terms_api = []
                    for t in group:
                        if " " in t: group_terms_api.append(f'"{t}"')
                        else: group_terms_api.append(t)
                    api_term_groups.append(group_terms_api)
                
                q_list_nat = [" ".join(nat_parts)]
                # API 组合逻辑: (A|B) + (C|D) -> A C, A D, B C, B D
                product_tuples = list(itertools.product(*api_term_groups))
                q_list_api = [" ".join(t) for t in product_tuples]
                st.info(f"🔍 高级模式: Nature '{q_list_nat[0]}'; API 组合 {len(q_list_api)} 次")
                
            else:
                q_list_nat = []
                q_list_api = []
                filter_kws_struct = None 
                for group in raw_kws:
                    terms = [t.strip() for t in group.split('/') if t.strip()]
                    processed = [f'"{t}"' if " " in t else t for t in terms]
                    if len(processed) > 1: nat_q = "(" + " OR ".join(processed) + ")"
                    else: nat_q = processed[0]
                    q_list_nat.append(nat_q)
                    q_list_api.extend(processed)
                st.info(f"🔍 普通模式: Nature {len(q_list_nat)} 组; API {len(q_list_api)} 词")

            clash_cfg = {"enabled": auto_rotate, "url": clash_url.rstrip('/'), "secret": clash_sec, "group": rot_grp, "nodes": avail_nodes}
            prox_list = st.session_state.proxy_manager.proxies if use_proxy else []
            
            stat = st.status("正在检索...", expanded=True)
            all_logs = []
            nat_res = []
            api_res = []
            
            # 1. 准备任务
            nature_tasks = []
            if sel_nat_map:
                nature_tasks = prepare_nature_tasks(q_list_nat, sel_nat_map, s_y, e_y, use_proxy, prox_list, user_cookie, clash_cfg, en_sch, en_abs, filter_kws_struct, nat_pages, strict_filter)
            
            api_tasks = []
            if ignore_venue_filter or sel_api:
                api_tasks = prepare_api_tasks(q_list_api, s_y, e_y, lim, sel_api, use_proxy, prox_list, filter_kws_struct, strict_filter, ignore_venue_filter)

            # 2. 进度条 UI
            st.markdown("#### 🚀 检索进度")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown("**Nature 官网**")
                nat_prog = st.progress(0)
                nat_txt = st.empty()
            with col_p2:
                st.markdown("**IEEE/Science API**")
                api_prog = st.progress(0)
                api_txt = st.empty()
            
            # 3. 统一线程池执行
            total_workers = 15
            with concurrent.futures.ThreadPoolExecutor(max_workers=total_workers) as executor:
                future_to_type = {}
                
                # Submit Nature
                nat_total = len(nature_tasks)
                nat_done = 0
                for task in nature_tasks:
                    fut = executor.submit(scrape_nature_worker, task)
                    future_to_type[fut] = ('nature', task)
                
                # Submit API
                api_total = len(api_tasks)
                api_done = 0
                for task in api_tasks:
                    fut = executor.submit(search_api_worker, task)
                    future_to_type[fut] = ('api', task)
                
                # As Completed Loop
                for future in concurrent.futures.as_completed(future_to_type):
                    t_type, t_info = future_to_type[future]
                    try:
                        r_list, err, l_list = future.result()
                        if l_list: all_logs.extend(l_list)
                        if r_list:
                            if t_type == 'nature': nat_res.extend(r_list)
                            else:
                                q_kw = t_info[0]  # query string used for this API call
                                api_res.extend([normalize_api_result(p, q_kw) for p in r_list])
                        
                        if t_type == 'nature':
                            nat_done += 1
                            if nat_total > 0: 
                                nat_prog.progress(nat_done/nat_total)
                                nat_txt.markdown(f"<div style='text-align:right; color:gray; font-size:0.8em'>{t_info[1]}</div>", unsafe_allow_html=True)
                        else:
                            api_done += 1
                            if api_total > 0: 
                                api_prog.progress(api_done/api_total)
                                v_disp = "Global" if t_info[8] else (t_info[4][0][:15]+"..." if t_info[4] else "All")
                                api_txt.markdown(f"<div style='text-align:right; color:gray; font-size:0.8em'>{v_disp}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        all_logs.append(f"Main Loop Err: {e}")

            nat_prog.progress(1.0)
            api_prog.progress(1.0)
            
            results = nat_res + api_res
            st.session_state['last_results'] = results
            st.session_state['last_logs'] = all_logs
            st.session_state['last_filter_struct'] = filter_kws_struct
            stat.update(label="完成", state="complete", expanded=False)

    # --- 结果展示 ---
    if 'last_results' in st.session_state and st.session_state['last_results']:
        results = st.session_state['last_results']
        logs = st.session_state.get('last_logs', [])
        filter_struct = st.session_state.get('last_filter_struct', None)
        if 'removed_items' not in st.session_state:
            st.session_state['removed_items'] = set()
        if 'selected_items' not in st.session_state:
            st.session_state['selected_items'] = set()
        removed = st.session_state['removed_items']
        selected = st.session_state['selected_items']
        
        # 本地过滤 (Strict)
        if strict_filter and filter_struct:
            filtered_results = []
            for p in results:
                content = (p['Title'] + " " + (p['Abstract'] or "")).lower()
                is_match = True
                for group in filter_struct:
                    group_match = False
                    for k in group:
                        clean_k = k.replace('"', '').replace("'", "").lower()
                        if clean_k in content:
                            group_match = True
                            break
                    if not group_match:
                        is_match = False
                        break
                if is_match: filtered_results.append(p)
            display_results = filtered_results
            st.caption(f"🔍 严格过滤: {len(results)} -> {len(display_results)}")
        else:
            display_results = results

        # 本地删除过滤
        display_results = [p for p in display_results if item_key(p) not in removed]

        if logs:
            with st.expander("📝 运行日志", expanded=False):
                for l in logs:
                    if "Full Abs" in l: st.markdown(f":blue[{l}]")
                    elif "Found" in l or "Success" in l: st.markdown(f":green[{l}]")
                    elif "Redirected" in l or "Error" in l or "Status" in l: st.markdown(f":red[{l}]")
                    else: st.text(l)

        df_raw = pd.DataFrame(display_results)
        if not df_raw.empty:
            if 'Journal' not in df_raw.columns and 'venue' in df_raw.columns:
                df_raw['Journal'] = df_raw['venue']
            if 'Journal' in df_raw.columns and 'venue' in df_raw.columns:
                # Replace empty/placeholder Journal with venue when available
                mask_unknown = df_raw['Journal'].astype(str).str.strip().isin(['', 'Unknown', 'nan'])
                df_raw.loc[mask_unknown, 'Journal'] = df_raw.loc[mask_unknown, 'venue']
            if 'Journal' in df_raw.columns:
                df_raw['Journal'] = df_raw['Journal'].fillna('Unknown').astype(str)
            if 'FullJournal' not in df_raw.columns and 'Journal' in df_raw.columns:
                df_raw['FullJournal'] = df_raw['Journal']
            df_raw['SortYear'] = pd.to_numeric(df_raw['Year'], errors='coerce').fillna(0)

            df = deduplicate_dataframe(df_raw)
            dedup_removed = len(df_raw) - len(df)
            df = add_translate_key(df, "online")
            df = apply_cn_column(df)
            df = df.sort_values(by=['SortYear', 'DisplayDate'], ascending=[False, False])
            
            msg = f"🎉 共找到 {len(df)} 篇论文"
            if dedup_removed > 0: msg += f"（已自动去重 {dedup_removed} 篇）"
            st.success(msg)
            
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                st.download_button("📥 导出 CSV", df.to_csv(index=False).encode('utf-8-sig'), "papers_final.csv", use_container_width=True)
            with col_act2:
                if st.button("🌐 批量翻译摘要", key="batch_translate_online", use_container_width=True):
                    df, count = batch_translate(df, max_workers=1000)
                    if count == 0: st.info("暂无需要翻译的摘要")
                    else:
                        st.success(f"翻译完成 {count} 篇摘要")
                        st.rerun()
            with col_act3:
                if st.button("🗑️ 批量删除选中", key="batch_del_online", use_container_width=True):
                    if selected:
                        removed.update(selected)
                        selected.clear()
                        st.rerun()
            
            journals = sorted(df['Journal'].unique())
            tabs = st.tabs([f"{j} ({len(df[df['Journal']==j])})" for j in journals])
            
            for i, j_name in enumerate(journals):
                with tabs[i]:
                    sub = df[df['Journal'] == j_name]
                    for idx, r in sub.iterrows():
                        # 复合键解决 Duplicate Key
                        key = r['TranslateKey'] if 'TranslateKey' in r else f"online_{idx}_{hash(r['Title'])}"
                        cite_val = r['Citations'] if 'Citations' in r else "N/A"
                        if str(cite_val) in ["N/A", "0", "0.0", "nan", "None", "", "None"]:
                            cite_badge = '<span class="badge badge-cite" style="background:linear-gradient(135deg,#9ca3af,#6b7280)">Cite: Unknown</span>'
                        else:
                            cite_badge = f'<span class="badge badge-cite">🔥 Cite: {cite_val}</span>'
                        
                        # --- 美化后的卡片式布局 ---
                        with st.container():
                            card_html = textwrap.dedent(f"""
                                <div class="paper-card">
                                    <h4>{r['Title']}</h4>
                                    <div style="margin-bottom: 10px;">
                                        <span class="badge badge-year">{r['Year']}</span>
                                        <span class="badge badge-journal">{r['Journal']}</span>
                                        {cite_badge}
                                        <span style="color: gray; font-size: 0.9em; margin-left: 5px;">📅 {r['DisplayDate']}</span>
                                    </div>
                                </div>
                            """).strip()
                            st.markdown(card_html, unsafe_allow_html=True)
                            
                            c1, c2 = st.columns([0.05, 0.95])
                            with c1:
                                sel_val = st.checkbox("", key=f"sel_{key}", value=(key in selected), label_visibility="collapsed")
                                if sel_val: selected.add(key)
                                else: selected.discard(key)
                            
                            with c2:
                                abst = r['Abstract']
                                if not abst: abst = "暂无摘要"
                                cn_txt = r.get('Abstract_CN')
                                
                                # 摘要区域
                                if cn_txt and str(cn_txt).strip():
                                    st.info(cn_txt)
                                    with st.expander("📄 查看英文原文"): st.write(abst)
                                else:
                                    with st.expander("📄 查看摘要", expanded=False):
                                        st.write(abst)
                                        if abst != "暂无摘要":
                                            if st.button("🌐 翻译", key=f"btn_{key}"):
                                                with st.spinner("Translating..."):
                                                    res = translate_text_deepseek(abst)
                                                    st.session_state['translations'][key] = res
                                                    st.rerun()
                                
                                # 底部操作栏
                                col_meta1, col_meta2 = st.columns([4, 1])
                                with col_meta1:
                                    match_list = find_matched_terms(str(r['Title']), str(r['Abstract']) if r['Abstract'] else "", filter_struct if strict_filter else None)
                                    match_disp = ", ".join(match_list) if match_list else r.get('MatchKeyword', 'N/A')
                                    st.caption(f"Match: {match_disp} | Src: {r['Source']}")
                                with col_meta2:
                                    col_lnk, col_del = st.columns(2)
                                    with col_lnk:
                                        url_val = r.get('URL') if 'URL' in r else None
                                        if pd.notna(url_val) and str(url_val).strip():
                                            st.link_button("🔗", str(url_val), help="Read Paper")
                                    with col_del:
                                        if st.button("🗑️", key=f"del_{key}", help="Remove Item"):
                                            st.session_state['removed_items'].add(key)
                                            st.rerun()
        else:
            st.warning("⚠️ 暂无搜索结果")

# ================= 模式 2: 结果分析 (Preview) =================
elif app_mode == "📂 结果分析(Preview)":
    df = None
    with st.sidebar:
        st.divider()
        uploaded_file = st.file_uploader("📂 上传 CSV 1", type="csv")
        uploaded_file2 = st.file_uploader("📂 上传 CSV 2 (可选)", type="csv")
        dfs = []
        for idx, uf in enumerate([uploaded_file, uploaded_file2], start=1):
            if uf:
                try:
                    tmp_df = pd.read_csv(uf)
                    dfs.append(tmp_df)
                except Exception as e:
                    st.error(f"文件 {idx} 读取失败: {e}")
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            if len(dfs) > 1:
                st.info(f"已合并 {len(dfs)} 个文件，共 {len(df)} 条记录")

        if df is not None:
            if 'removed_items_preview' not in st.session_state:
                st.session_state['removed_items_preview'] = set()
            if 'selected_items_preview' not in st.session_state:
                st.session_state['selected_items_preview'] = set()
            if 'Journal' not in df.columns and 'venue' in df.columns:
                df['Journal'] = df['venue']
            if 'Year' not in df.columns and 'year' in df.columns:
                df['Year'] = df['year']
            if 'Title' not in df.columns and 'title' in df.columns:
                df['Title'] = df['title']
            if 'Citations' not in df.columns and 'citationCount' in df.columns:
                df['Citations'] = df['citationCount']
            if 'Abstract' not in df.columns and 'abstract' in df.columns:
                df['Abstract'] = df['abstract']
            if 'URL' not in df.columns and 'url' in df.columns:
                df['URL'] = df['url']
            if 'DisplayDate' not in df.columns and 'publicationDate' in df.columns:
                df['DisplayDate'] = df['publicationDate']
            # Backfill missing values row-wise when both columns exist
            if 'Journal' in df.columns and 'venue' in df.columns:
                df['Journal'] = df['Journal'].fillna(df['venue'])
                mask_unknown = df['Journal'].astype(str).str.strip().isin(['', 'Unknown', 'nan'])
                df.loc[mask_unknown, 'Journal'] = df.loc[mask_unknown, 'venue']
            if 'FullJournal' in df.columns and 'Journal' in df.columns:
                df['FullJournal'] = df['FullJournal'].fillna(df['Journal'])
            if 'Title' in df.columns and 'title' in df.columns:
                df['Title'] = df['Title'].fillna(df['title'])
            if 'Year' in df.columns and 'year' in df.columns:
                df['Year'] = df['Year'].fillna(df['year'])
            if 'Citations' in df.columns and 'citationCount' in df.columns:
                df['Citations'] = df['Citations'].fillna(df['citationCount'])
            if 'Abstract' in df.columns and 'abstract' in df.columns:
                df['Abstract'] = df['Abstract'].fillna(df['abstract'])
            if 'URL' in df.columns and 'url' in df.columns:
                df['URL'] = df['URL'].fillna(df['url'])
            if 'DisplayDate' in df.columns and 'publicationDate' in df.columns:
                df['DisplayDate'] = df['DisplayDate'].fillna(df['publicationDate'])
            if 'Journal' in df.columns:
                df['Journal'] = df['Journal'].fillna('Unknown').astype(str)
            if 'FullJournal' not in df.columns and 'Journal' in df.columns:
                df['FullJournal'] = df['Journal']
            # Normalize numeric fields for filtering/sorting
            if 'Year' in df.columns:
                df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
            if 'Citations' in df.columns:
                df['Citations'] = pd.to_numeric(df['Citations'], errors='coerce')
            
            sort_opt = st.radio("排序方式", ["年份", "引用"])
            all_journals = sorted(df['Journal'].astype(str).unique())
            sel_journals = st.multiselect("筛选期刊", all_journals, default=all_journals)
            year_series = df['Year'] if 'Year' in df.columns else pd.Series([0])
            min_y, max_y = int(year_series.min()), int(year_series.max())
            sel_years = st.slider("筛选年份", min_y, max_y, (min_y, max_y)) if min_y != max_y else (min_y, max_y)
            
            st.markdown("**本地严格过滤**")
            txt_filter = st.text_area("关键词 (A/B; C/D)", "", height=60)
            strict_mode = st.checkbox("启用过滤", False)

    if df is not None:
        if 'removed_items_preview' not in st.session_state:
            st.session_state['removed_items_preview'] = set()
        filter_struct = None
        df_filtered = df[
            (df['Journal'].isin(sel_journals)) & 
            (df['Year'] >= sel_years[0]) & 
            (df['Year'] <= sel_years[1])
        ]
        
        if strict_mode and txt_filter:
            filter_struct = []
            for grp in txt_filter.split(';'):
                terms = [t.strip().replace('"', '').replace("'", "") for t in grp.split('/') if t.strip()]
                if terms: filter_struct.append(terms)
            
            if filter_struct:
                filtered_indices = []
                for idx, row in df_filtered.iterrows():
                    title_txt = str(row['Title']) if pd.notna(row['Title']) else ""
                    abs_txt = str(row['Abstract']) if pd.notna(row['Abstract']) else ""
                    content = (title_txt + " " + abs_txt).lower()
                    is_match = True
                    for group in filter_struct:
                        if not any(k.lower() in content for k in group):
                            is_match = False
                            break 
                    if is_match: filtered_indices.append(idx)
                df_filtered = df_filtered.loc[filtered_indices]

        if "引用" in sort_opt:
            if 'Citations' in df_filtered.columns:
                df_filtered['Citations_Num'] = pd.to_numeric(df_filtered['Citations'], errors='coerce').fillna(0)
                df_filtered = df_filtered.sort_values(by='Citations_Num', ascending=False)
        else:
            df_filtered = df_filtered.sort_values(by='Year', ascending=False)

        pre_dedup_len = len(df_filtered)
        df_filtered = deduplicate_dataframe(df_filtered)
        dedup_removed = pre_dedup_len - len(df_filtered)
        df_filtered = add_translate_key(df_filtered, "local")
        df_filtered = apply_cn_column(df_filtered)
        # 删除过滤
        df_filtered = df_filtered[~df_filtered.apply(lambda r: item_key(r, prefix="local") in st.session_state['removed_items_preview'], axis=1)]
        
        # Header area
        st.markdown(f"### 📂 共找到 {len(df_filtered)} 篇论文" + (f" <span style='font-size:0.6em;color:gray'>（去重 {dedup_removed}）</span>" if dedup_removed > 0 else ""), unsafe_allow_html=True)
        
        col_act1, col_act2, col_act3 = st.columns(3)
        with col_act1:
            st.download_button("📥 导出筛选结果", df_filtered.to_csv(index=False).encode('utf-8-sig'), "papers_preview_filtered.csv", use_container_width=True)
        with col_act2:
            if st.button("🌐 批量翻译 (本地)", key="batch_translate_local", use_container_width=True):
                df_filtered, count = batch_translate(df_filtered, max_workers=1000)
                if count == 0: st.info("暂无需要翻译的摘要")
                else:
                    st.success(f"翻译完成 {count} 篇摘要")
                    st.rerun()
        with col_act3:
            if st.button("🗑️ 批量删除 (本地)", key="batch_del_local", use_container_width=True):
                sel_prev = st.session_state['selected_items_preview']
                if sel_prev:
                    st.session_state['removed_items_preview'].update(sel_prev)
                    sel_prev.clear()
                    st.rerun()
        
        journals_f = sorted(df_filtered['Journal'].unique())
        if not journals_f: st.warning("⚠️ 无结果")
        else:
            tabs = st.tabs([f"{j} ({len(df_filtered[df_filtered['Journal']==j])})" for j in journals_f])
            for i, j_name in enumerate(journals_f):
                with tabs[i]:
                    sub = df_filtered[df_filtered['Journal'] == j_name]
                    for idx, r in sub.iterrows():
                        # 复合键解决 Duplicate Key (Preview 模式)
                        key = r['TranslateKey'] if 'TranslateKey' in r else f"local_{idx}_{hash(str(r['Title']))}"
                        cite_val = r['Citations'] if 'Citations' in r else "N/A"
                        if str(cite_val) in ["N/A", "0", "0.0", "nan", "None", "", "None"]:
                            cite_badge = '<span class="badge badge-cite" style="background:linear-gradient(135deg,#9ca3af,#6b7280)">Cite: Unknown</span>'
                        else:
                            cite_badge = f'<span class="badge badge-cite">🔥 Cite: {cite_val}</span>'
                        
                        # --- 美化后的卡片式布局 ---
                        with st.container():
                            card_html = textwrap.dedent(f"""
                                <div class="paper-card">
                                    <h4>{r['Title']}</h4>
                                    <div style="margin-bottom: 10px;">
                                        <span class="badge badge-year">{r['Year']}</span>
                                        <span class="badge badge-journal">{r['Journal']}</span>
                                        {cite_badge}
                                        <span style="color: gray; font-size: 0.9em; margin-left: 5px;">📅 {r.get('DisplayDate', r['Year'])}</span>
                                    </div>
                                </div>
                            """).strip()
                            st.markdown(card_html, unsafe_allow_html=True)

                            c1, c2 = st.columns([0.05, 0.95])
                            with c1:
                                sel_val = st.checkbox("", key=f"sel_local_{key}", value=(key in st.session_state['selected_items_preview']), label_visibility="collapsed")
                                if sel_val: st.session_state['selected_items_preview'].add(key)
                                else: st.session_state['selected_items_preview'].discard(key)
                            
                            with c2:
                                abst = r['Abstract'] if pd.notna(r['Abstract']) else "暂无摘要"
                                cn_txt = r.get('Abstract_CN')
                                
                                if cn_txt and str(cn_txt).strip():
                                    st.info(cn_txt)
                                    with st.expander("📄 查看英文原文"): st.write(abst)
                                else:
                                    with st.expander("📄 查看摘要", expanded=False):
                                        st.write(abst)
                                        if abst != "暂无摘要":
                                            if st.button("🌐 翻译", key=f"btn_{key}"):
                                                with st.spinner("Translating..."):
                                                    res = translate_text_deepseek(abst)
                                                    st.session_state['translations'][key] = res
                                                    st.rerun()
                                
                                col_meta1, col_meta2 = st.columns([4, 1])
                                with col_meta1:
                                    match_list = find_matched_terms(str(r['Title']), str(abst), filter_struct if strict_mode else None)
                                    match_disp = ", ".join(match_list) if match_list else r.get('MatchKeyword', 'N/A')
                                    st.caption(f"Match: {match_disp} | Src: {r.get('Source', 'Local')}")
                                with col_meta2:
                                    col_lnk, col_del = st.columns(2)
                                    with col_lnk:
                                        url = r['URL'] if pd.notna(r['URL']) else None
                                        if url: st.link_button("🔗", url, help="Read Paper")
                                    with col_del:
                                        if st.button("🗑️", key=f"del_local_{key}", help="Remove Item"):
                                            st.session_state['removed_items_preview'].add(key)
                                            st.rerun()

    else:
        if app_mode == "📂 结果分析(Preview)": st.info("👈 请在左侧上传 CSV 文件")
