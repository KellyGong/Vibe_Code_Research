#!/usr/bin/env python3
"""
使用 DeepSeek API 批量阅读 PDF 论文，并按新的 Survey Outline 生成思维导图。

Outline:
1) Representation: Aligning Modalities with Chemical Nature
2) Cognition: Mechanisms of Knowledge Acquisition and Reasoning
3) Application: A Hierarchical Taxonomy of Chemical Tasks

输出:
- 单篇论文: JSON + XMind Markdown (paper_mindmaps/)
- 按 subsubsection 聚合: 多个 XMind Markdown (by_subsubsection/)

额外要求:
- 从 ref.bib 中匹配论文 title -> citekey(bib key)，在每个节点保留 title + key
"""

from __future__ import annotations

import json
import os
import random
import re
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any, Dict, Iterable, List, Optional, Tuple

import fitz  # PyMuPDF
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)
from tqdm import tqdm

# Script directory (for resolving relative default paths)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# DeepSeek API 配置
API_KEYS_FILE = os.path.join(_SCRIPT_DIR, "deepseek_keys.txt")
BASE_URL = "https://api.deepseek.com"

# BibTeX（用于 title -> key）
BIB_FILE = os.path.join(_SCRIPT_DIR, "ref.bib")

# PDF 目录
PDF_DIRS = [
    "./downloads",
    "./nature_pdfs",
]

# 输出目录
OUTPUT_ROOT = "./mindmap_output"
PAPER_JSON_DIR = os.path.join(OUTPUT_ROOT, "paper_json")
PAPER_MINDMAP_DIR = os.path.join(OUTPUT_ROOT, "paper_mindmaps")
SUBSUBSECTION_DIR = os.path.join(OUTPUT_ROOT, "by_subsubsection")

DEFAULT_MAX_WORKERS = 200
DEFAULT_MAX_RETRIES = 6
DEFAULT_PER_KEY_CONCURRENCY_CAP = 20

UNRELATED_ROOT = os.path.join(OUTPUT_ROOT, "unrelated")
UNRELATED_JSON_DIR = os.path.join(UNRELATED_ROOT, "paper_json")
UNRELATED_MINDMAP_DIR = os.path.join(UNRELATED_ROOT, "paper_mindmaps")
TOPIC_FILTER_LOG = os.path.join(OUTPUT_ROOT, "topic_filter_results.jsonl")


REP_SECTION = "Representation: Aligning Modalities with Chemical Nature"
COG_SECTION = "Cognition: Mechanisms of Knowledge Acquisition and Reasoning"
APP_SECTION = "Application: A Hierarchical Taxonomy of Chemical Tasks"

REP_SUBSECTIONS: Dict[str, List[str]] = {
    "Linguistic Linearization: The Grammar of Chemistry": [
        "Adaptive Tokenization Granularity",
        "Syntax-Robust Linearization",
        "Augmentation-Driven Semantic Alignment",
    ],
    "Topological Perception: Incorporating Structural Bias": [
        "Graph Serialization",
        "Graph-Text Projectors",
        "Graph-Injected Architectures",
    ],
    "Geometric Grounding: Encoding Physical Reality": [
        "Coordinate",
        "Geometric Encoders and Fusion",
        "Point Cloud and Surface Alignment",
    ],
}

COG_SUBSECTIONS: Dict[str, List[str]] = {
    "Internalization: Cultivating Parametric Chemical Intuition": [
        "Imbibing Chemical Syntax and Semantics",
        "Aligning Capabilities with Expert Intent",
        "Aligning Generative Behavior with Physical Objectives",
    ],
    "Externalization: Anchoring to Physical Reality via Interfacing": [
        'Knowledge Augmentation: Querying the "Static World"',
        'Tool Orchestration: Leveraging the "Calculable World"',
        'Empirical Feedback: interacting with the "Physical World"',
    ],
    "Reasoning: Cognitive Frameworks for Chemical Logic": [
        "Inferring Patterns via Contextual Analogy",
        "Deciphering Causality via Sequential Deduction",
        "Traversing Combinatorial Spaces via Strategic Planning",
        "Enforcing Validity via Introspective Refinement",
    ],
}

# reverse mapping for robust normalization when the model outputs wrong "subsection"
COG_SUBSUB_TO_SUBSECTION: Dict[str, str] = {}
for _sub, _subs in COG_SUBSECTIONS.items():
    for _ss in _subs:
        COG_SUBSUB_TO_SUBSECTION[_ss] = _sub

APP_TASKS: List[str] = [
    "Bridging Modal Gaps via Semantic Translation",
    "Deciphering Hidden Properties via Discriminative Inference",
    "Sculpting Novel Structures under Functional Constraints",
    "Orchestrating Causal Pathways for Autonomous Discovery",
]


def load_api_keys() -> List[str]:
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def create_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def extract_text_from_pdf(pdf_path: str, max_pages: int = 20, max_chars: int = 50000) -> str:
    try:
        doc = fitz.open(pdf_path)
        text_parts: List[str] = []
        for page_num in range(min(len(doc), max_pages)):
            page = doc[page_num]
            text_parts.append(page.get_text())
        doc.close()
        full_text = "\n".join(text_parts)
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars] + "\n...[内容已截断]"
        return full_text
    except Exception as e:
        return f"Error extracting text: {e}"


def normalize_for_match(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\\[a-zA-Z]+", " ", text)  # latex commands
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_bib_title(title: str) -> str:
    if not title:
        return ""
    # remove outer braces used for capitalization, keep content
    title = title.replace("{", "").replace("}", "")
    # de-escape common sequences
    title = title.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_")
    # drop simple latex command names (keep arguments already kept by brace removal)
    title = re.sub(r"\\[a-zA-Z]+", "", title)
    return re.sub(r"\s+", " ", title).strip()


def score_title_match(a_norm: str, b_norm: str) -> float:
    if not a_norm or not b_norm:
        return 0.0
    ratio = SequenceMatcher(None, a_norm, b_norm).ratio()
    a_tokens = set(a_norm.split())
    b_tokens = set(b_norm.split())
    token_overlap = 0.0
    if a_tokens and b_tokens:
        token_overlap = len(a_tokens & b_tokens) / max(len(a_tokens), len(b_tokens))
    return 0.65 * ratio + 0.35 * token_overlap


def closest_choice(value: str, choices: Iterable[str]) -> Tuple[Optional[str], float]:
    value_norm = normalize_for_match(value)
    best_choice: Optional[str] = None
    best_score = 0.0
    for c in choices:
        c_norm = normalize_for_match(c)
        if not c_norm:
            continue
        score = score_title_match(value_norm, c_norm)
        if score > best_score:
            best_score = score
            best_choice = c
    return best_choice, best_score


def candidate_titles_from_filename(paper_name: str) -> List[str]:
    base = paper_name.replace("_", " ").strip()
    candidates = [base]
    if "-" in paper_name:
        parts = paper_name.split("-")
        for i in range(1, min(4, len(parts))):
            candidates.append("-".join(parts[i:]).replace("_", " ").strip())
    # de-duplicate while keeping order
    seen = set()
    out: List[str] = []
    for c in candidates:
        c_norm = normalize_for_match(c)
        if not c_norm or c_norm in seen:
            continue
        seen.add(c_norm)
        out.append(c)
    return out


def extract_bib_field(entry_body: str, field: str) -> Optional[str]:
    m = re.search(rf"(?i)\b{re.escape(field)}\s*=\s*", entry_body)
    if not m:
        return None
    i = m.end()
    while i < len(entry_body) and entry_body[i].isspace():
        i += 1
    if i >= len(entry_body):
        return None
    if entry_body[i] == "{":
        depth = 1
        i += 1
        start = i
        while i < len(entry_body) and depth > 0:
            ch = entry_body[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            i += 1
        return entry_body[start : i - 1].strip()
    if entry_body[i] == '"':
        i += 1
        start = i
        while i < len(entry_body):
            ch = entry_body[i]
            if ch == '"' and entry_body[i - 1] != "\\":
                break
            i += 1
        return entry_body[start:i].strip()
    # bare word
    start = i
    while i < len(entry_body) and entry_body[i] not in ",\n\r":
        i += 1
    return entry_body[start:i].strip()


@dataclass(frozen=True)
class BibEntry:
    key: str
    title_raw: str
    title_clean: str
    title_norm: str


def parse_bibtex_file(bib_path: str) -> List[BibEntry]:
    if not os.path.exists(bib_path):
        return []
    with open(bib_path, "r", encoding="utf-8") as f:
        text = f.read()

    entries: List[BibEntry] = []
    # 用 ^@ 分割更鲁棒：避免某些abstract里括号/大括号不配对导致整文件解析中断
    starts = [m.start() for m in re.finditer(r"(?m)^@", text)]
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if (idx + 1) < len(starts) else len(text)
        chunk = text[start:end].strip()
        if not chunk:
            continue

        brace = chunk.find("{")
        paren = chunk.find("(")
        if brace == -1 and paren == -1:
            continue
        open_pos = brace if (brace != -1 and (paren == -1 or brace < paren)) else paren

        comma = chunk.find(",", open_pos + 1)
        if comma == -1:
            continue
        key = chunk[open_pos + 1 : comma].strip()
        if not key:
            continue

        body = chunk[comma + 1 :]
        title_raw = extract_bib_field(body, "title") or ""
        title_clean = clean_bib_title(title_raw)
        title_norm = normalize_for_match(title_clean)
        entries.append(
            BibEntry(key=key, title_raw=title_raw, title_clean=title_clean, title_norm=title_norm)
        )

    return entries


def match_bib_by_title(paper_name: str, bib_entries: List[BibEntry]) -> Tuple[Optional[BibEntry], float]:
    candidates = candidate_titles_from_filename(paper_name)
    best_entry: Optional[BibEntry] = None
    best_score = 0.0
    for cand in candidates:
        cand_norm = normalize_for_match(cand)
        for entry in bib_entries:
            if not entry.title_norm:
                continue
            score = score_title_match(cand_norm, entry.title_norm)
            if score > best_score:
                best_score = score
                best_entry = entry
    return best_entry, best_score


def safe_slug(text: str, max_len: int = 120) -> str:
    text = text.strip()
    if not text:
        return "unknown"
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:max_len] if len(text) > max_len else text


def ensure_dirs() -> None:
    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    os.makedirs(PAPER_JSON_DIR, exist_ok=True)
    os.makedirs(PAPER_MINDMAP_DIR, exist_ok=True)
    os.makedirs(SUBSUBSECTION_DIR, exist_ok=True)
    os.makedirs(UNRELATED_ROOT, exist_ok=True)
    os.makedirs(UNRELATED_JSON_DIR, exist_ok=True)
    os.makedirs(UNRELATED_MINDMAP_DIR, exist_ok=True)


def extract_json_block(content: str) -> str:
    m = re.search(r"<json>(.*?)</json>", content, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # strip markdown code fences if any
    text = content.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    # try to find outermost json object
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1].strip()
    return text


def load_json_maybe_dirty(path: str) -> Any:
    """
    读取 JSON 文件：优先严格解析；若文件包含非法utf-8字节或末尾拼接了额外文本/JSON，
    尝试用 JSONDecoder.raw_decode 提取第一个 JSON 对象作为兜底。
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        raw = open(path, "rb").read().decode("utf-8", errors="replace")
        try:
            return json.loads(raw)
        except Exception:
            obj, _ = json.JSONDecoder().raw_decode(raw.lstrip())
            return obj


def analyze_paper(client: OpenAI, paper_text: str, bib_key: str, title: str) -> Dict[str, Any]:
    rep_tax = "\n".join(
        [f'- "{sub}": {json.dumps(items, ensure_ascii=False)}' for sub, items in REP_SUBSECTIONS.items()]
    )
    cog_tax = "\n".join(
        [f'- "{sub}": {json.dumps(items, ensure_ascii=False)}' for sub, items in COG_SUBSECTIONS.items()]
    )
    app_tax = json.dumps(APP_TASKS, ensure_ascii=False)

    prompt = f"""你是一个严谨的学术论文阅读助手，目标是为一篇 Survey 构建可合并的“分级思维导图节点”。

论文元信息（来自bib/ref，不要改写）：
- bib_key: {bib_key}
- title: {title}

论文内容（节选，可能截断）：
{paper_text}

请按以下 Survey Outline 归类并总结。
硬性要求：
- 每篇论文必须覆盖 Cognition 和 Application
- Representation 至少 1 条（即使不是贡献点，也要总结它采用的表示方式）
- Cognition/Reasoning 也必须给出对应的 Contribution（若确实没有可为空列表）

关键归类规则（用于提升归类一致性）：
0) Representation 归类按“分子信息主要以什么形式进入模型”：
   - 显式3D坐标/XYZ/构象/点云/表面 -> Geometric Grounding（优先选 Coordinate/Point Cloud/Geometric Encoders）
   - 纯文本线性化（SMILES/SELFIES/IUPAC/反应式等）及其tokenization/增强 -> Linguistic Linearization
     注意：只要论文的“主要分子表示”是 SMILES/SELFIES/IUPAC 等字符串，也一律归到 Linguistic Linearization。
   - 分子图/拓扑结构（原子/键）以图形式进入模型 -> Topological Perception
     Topological Perception 的三个 subsubsection 请严格按以下定义区分：
     1) Graph Serialization：
        仅当论文【把分子图/拓扑结构离散化】为 tokens/序列/自然语言描述/图文法 等“可被序列模型/LLM直接读的离散符号”时，才归到这里。
        典型信号：节点/边 token、DFS/BFS 遍历序列、graph-to-text、子结构 token 化、图语法离散编码、无损/可逆的图序列化表示等。
        不要把“普通 SMILES/SELFIES 字符串表示”归到这里（那属于 Linguistic Linearization）。
        反例：仅用 GNN/GraphTransformer 编码成连续向量、或仅在注意力里加 edge-bias，这些都【不属于】Graph Serialization。
     2) Graph-Text Projectors：
        论文使用图编码器（GNN/GraphTransformer 等）得到【连续向量】并通过 projector/adapter（线性层、MLP、cross-attn桥接模块等）注入到 LLM/文本空间；
        核心特征是“图->连续表征->投影/对齐到文本模态”，而不是把图离散成 token。
     3) Graph-Injected Architectures：
        剩余的“从模型架构层面原生支持图数据”的方法：例如修改注意力/层结构/消息传递，使 LM 内部直接处理图结构（edge-aware attn、relational bias、graph-attn 层、图结构注入的 transformer block 等）。
    - 3D几何信息（坐标/构象/点云/表面）-> Geometric Grounding，严格按以下规则区分三个 subsubsection：
     1) Coordinate：【仅限】大模型/LLM/Transformer 【直接】处理原始3D坐标作为输入（如将XYZ坐标token化、或作为连续embedding直接输入到主模型）。
        核心判断标准：3D坐标信息是否【不经过外置几何编码器】而直接进入主模型的注意力/transformer层。
        典型场景：坐标序列化为token、坐标直接作为位置编码、坐标作为额外输入维度拼接到token embedding等。
        【重要】如果论文使用了独立的3D encoder（如SchNet/DimeNet/E(3)-equivariant GNN/PointNet等）来预处理3D信息，则【不属于】Coordinate。
     2) Geometric Encoders and Fusion：使用【外置的几何编码器】（如E(3)-equivariant网络、SchNet、DimeNet、GemNet、PointNet、3D-GNN等）提取3D几何特征，然后通过fusion/projection模块与LLM/文本模态对齐或融合。
        核心特征：存在专门的3D几何编码器模块（通常具有旋转等变性、距离/角度感知等几何归纳偏置），其输出再与主模型融合。
        【关键】只要使用了外置encoder处理3D信息（无论是GNN、PointNet还是等变网络），都归到这里，不要归到Coordinate。
     3) Point Cloud and Surface Alignment：处理分子表面、静电势表面、溶剂可及表面、点云采样等"表面级"或"场级"的3D表示（而非单纯的原子坐标）。
        典型场景：表面网格、体素化、电子密度场、静电势场、表面点云、Gaussian splatting等。
   如果同时使用2D+3D，请至少包含一条 Geometric Grounding->Coordinate。
1) 先判断该论文是否“有训练”（是否更新模型参数）。如果完全没训练（纯prompt/ICL/RAG/工具/搜索/agent等，不更新参数）：
   - cognition 里【不允许】出现任何 Internalization 条目
   - cognition 里【必须】至少有一条 Externalization 条目（RAG / Tool / Empirical）
2) 如果“有训练”（Pretraining/SFT/Instruction tuning/RL等更新参数）：
   - cognition 里【必须】至少有一条 Internalization 条目
   - Externalization 仅用于“推理/使用阶段”的接口化增强（RAG/KB、tool calling/agentic orchestration、真实实验反馈闭环等）；如果没有这些，不要输出 Externalization。
3) Internalization 的三个 subsubsection 定义（必须严格按定义归类）：
   - Imbibing Chemical Syntax and Semantics：Pretraining 或普通 SFT（监督/多任务/蒸馏等）学习化学语法语义/分布（不是 instruction 数据/偏好对齐）
   - Aligning Capabilities with Expert Intent：Instruction tuning / preference alignment（如DPO/CPO/KTO/RLHF式偏好对齐等），强调“指令格式+专家意图对齐”
   - Aligning Generative Behavior with Physical Objectives：强化学习/奖励优化（PPO/REINFORCE等）直接优化物理/化学目标（如docking score、性质reward、合成可行性reward等）
4) 如果论文同时有 instruction tuning + RL，请拆成两条 Internalization，分别重点写 instruction tuning 细节 和 RL 细节。
5) 重要澄清：很多论文会做“任务特定的监督微调/回归/分类/翻译”等，这依然属于 Imbibing（普通SFT），只有明确的“指令格式数据/对话助手/偏好对齐”才归到 Aligning Capabilities。

## Taxonomy（分类名必须严格使用下面给定的英文字符串，summary/细节用中文）

### Representation: {REP_SECTION}
Subsection -> Subsubsection:
{rep_tax}

### Cognition: {COG_SECTION}
Subsection -> Subsubsection:
{cog_tax}

### Application: {APP_SECTION}
Task (choose one or more):
{app_tax}

## 输出格式（只输出 JSON，并用 <json>...</json> 包裹；不要输出任何解释/多余文字）

<json>
{{
  "paper": {{
    "bib_key": "{bib_key}",
    "title": "{title}",
    "method_name": "若有方法名/框架名则写，否则写空字符串"
  }},
  "representation": [
    {{
      "subsection": "从Representation三个subsection中选1个",
      "subsubsection": "从该subsection的subsubsection中选1个（字符串，不要用列表；如需多个类别请新增多条对象）",
      "summary": "一句话概括该论文的表示/对齐方式（中文）",
      "details": ["2-4条关键细节（中文，尽量具体）"],
      "contributions": ["0-3条贡献点（中文，若不是贡献可为空列表）"]
    }}
  ],
  "cognition": [
    {{
      "subsection": "从Cognition三个subsection中选1个（如需多个请新增多条对象）",
      "subsubsection": "对应的subsubsection（字符串）",
      "summary": "一句话概括其知识获取/对齐/推理机制（中文）",
      "details": ["2-4条关键细节（中文）"],
      "contributions": ["0-3条贡献点（中文，若没有可为空列表）"],
      "training_data": "训练/使用的数据（不清楚写未明确；training-free则写使用的基础模型/语料）",
      "objective_or_loss": "训练目标/损失（概括即可，不清楚写未明确）",
      "signals_or_tools": "外部信号/工具/反馈（没有写无）"
    }}
  ],
  "application": [
    {{
      "task": "必须从Application四个task里选",
      "summary": "一句话概括任务设置与目标（中文）",
      "datasets": ["数据集名称（若未给出写未明确）"],
      "metrics_or_results": ["指标/结果（没有具体数值也可以描述趋势）"],
      "scientific_findings": ["科学发现/洞见（没有写空列表）"]
    }}
  ]
}}
</json>

重要约束：
1) taxonomy字段必须严格使用给定英文字符串（否则无法合并）
2) 不要编造精确数值；未提及则写“未明确”
3) representation 至少 1 条；cognition 至少 1 条；application 至少 1 条
4) 完全没训练 -> cognition 只能包含 Externalization + Reasoning（不允许 Internalization）
5) 有训练 -> cognition 必须包含 Internalization；Externalization 仅在推理阶段确实使用RAG/工具/实验闭环时才写
6) Internalization 子类严格按定义：Pretraining/SFT->Imbibing；Instruction tuning/偏好对齐->Aligning Capabilities；RL/奖励优化->Aligning Generative Behavior
"""

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个专业的分子/化学AI论文阅读与分类助手。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=8192,
    )
    content = resp.choices[0].message.content or ""
    json_block = extract_json_block(content)
    data = json.loads(json_block)
    data = normalize_model_output(data, bib_key=bib_key, title=title)
    data["_usage"] = {
        "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
        "completion_tokens": getattr(resp.usage, "completion_tokens", None),
        "total_tokens": getattr(resp.usage, "total_tokens", None),
    }
    data["_raw"] = content
    return data


def _lower_compact(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip().lower()


def _join_item_text(item: Dict[str, Any], fields: List[str]) -> str:
    parts: List[str] = []
    for k in fields:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(v.strip())
    for k in ["details", "contributions"]:
        v = item.get(k)
        if isinstance(v, list):
            parts.extend([str(x).strip() for x in v if str(x).strip()])
    return _lower_compact(" ".join(parts))


def _contains_ascii_token(text_low: str, token: str) -> bool:
    """
    匹配短缩写（如 dpo/cpo/ipo）时避免误伤，例如 lipophilicity 含 'ipo' 子串。
    仅对 [a-z0-9] 进行“词边界”判断，中文/标点都会被视为边界。
    """
    if not token:
        return False
    return re.search(rf"(^|[^a-z0-9]){re.escape(token)}([^a-z0-9]|$)", text_low) is not None


def _internalization_stage(text_low: str) -> str:
    rl_strong_phrases = [
        "强化学习",
        "策略梯度",
        "actor-critic",
        "actor critic",
        "rl 微调",
        "rl fine-tuning",
    ]
    rl_strong_phrases += ["policy gradient"]
    rl_strong_tokens = ["ppo", "reinforce"]
    rl_weak_phrases = ["reinforcement learning", "rl", "策略优化", "奖励优化"]

    instr_phrases = [
        "instruction tuning",
        "instruction-tuning",
        "instruction-follow",
        "instruction following",
        "instruction fine-tuning",
        "instruction finetuning",
        "instruct",
        "指令微调",
        "指令调优",
        "指令对齐",
        "指令遵循",
        "指令数据",
        "指令格式",
        "instruction data",
        "偏好",
        "preference",
        "human feedback",
        "人类反馈",
    ]
    instr_tokens = ["rlhf", "rlaif", "dpo", "cpo", "kto", "ipo", "orpo"]

    physical_keywords = [
        "docking",
        "vina",
        "autodock",
        "binding affinity",
        "affinity",
        "binding energy",
        "qed",
        "sa",
        "synthesiz",
        "drug-likeness",
        "bioactivity",
        "ic50",
        "ec50",
        "ki",
        "kd",
        "对接",
        "亲和力",
        "结合能",
        "可合成",
        "合成可行",
        "药物相似",
        "活性",
        "毒性",
        "溶解度",
        "adme",
        "药代",
    ]

    has_rl_strong = any(k in text_low for k in rl_strong_phrases) or any(
        _contains_ascii_token(text_low, t) for t in rl_strong_tokens
    )
    has_rl_weak = any(k in text_low for k in rl_weak_phrases)
    has_physical = any(k in text_low for k in physical_keywords)
    has_instr = any(k in text_low for k in instr_phrases) or any(
        _contains_ascii_token(text_low, t) for t in instr_tokens
    )
    # 只有“RL + 物理/化学目标”才归入 Physical Objectives（避免把DPO/偏好对齐误判为RL）
    if (has_rl_strong or has_rl_weak) and has_physical:
        return "Aligning Generative Behavior with Physical Objectives"
    if has_instr:
        return "Aligning Capabilities with Expert Intent"
    # RL 但不是物理目标（常见于RLHF/偏好对齐等） -> 归到 Expert Intent
    if has_rl_strong or has_rl_weak:
        return "Aligning Capabilities with Expert Intent"
    return "Imbibing Chemical Syntax and Semantics"


def _externalization_subsubsection(text_low: str) -> str:
    # order matters: retrieval > empirical > tool
    if any(
        k in text_low
        for k in [
            "rag",
            "retriev",
            "检索",
            "搜索",
            "知识库",
            "knowledge base",
            "database",
            "kb",
            "pubchem",
            "chembl",
            "wikipedia",
        ]
    ):
        return 'Knowledge Augmentation: Querying the "Static World"'
    if any(k in text_low for k in ["实验", "wet-lab", "wet lab", "robot", "自动实验", "闭环实验", "active learning lab"]):
        return 'Empirical Feedback: interacting with the "Physical World"'
    if any(
        k in text_low
        for k in [
            "tool",
            "工具",
            "api",
            "调用",
            "agent",
            "agentic",
            "执行代码",
            "python",
            "rdkit",
            "openbabel",
            "simulation",
            "simulator",
            "docking",
            "namd",
            "gromacs",
            "orca",
            "gaussian",
        ]
    ):
        return 'Tool Orchestration: Leveraging the "Calculable World"'
    return 'Knowledge Augmentation: Querying the "Static World"'


def _looks_training_free_internalization(item: Dict[str, Any]) -> bool:
    """
    仅用于“兜底修正”旧数据：当 Internalization 项几乎没有任何训练证据时，
    将其移入 Externalization（prompt/ICL/RAG/tool/agent 等）。
    """
    td = (item.get("training_data") or "").strip()
    ol = (item.get("objective_or_loss") or "").strip()
    text_low = _join_item_text(item, ["summary", "training_data", "objective_or_loss", "signals_or_tools"])

    td_is_base = td in {"使用的基础模型/语料", "基础模型/语料", "base model", "foundation model"}
    ol_unknown = (not ol) or (ol in {"未明确", "无"})
    hints = any(
        k in text_low
        for k in [
            "prompt",
            "提示",
            "in-context",
            "上下文",
            "few-shot",
            "zero-shot",
            "training-free",
            "无需训练",
            "不涉及训练",
            "不进行训练",
            "不更新参数",
            "无需微调",
            "不微调",
            "不训练",
            "rag",
            "retriev",
            "检索",
            "tool",
            "工具",
            "agent",
            "代理",
            "workflow",
            "pipeline",
            "执行代码",
        ]
    )
    # 更鲁棒的“无训练”描述（允许中间插词）
    neg_train = re.search(r"(不|无需).{0,20}(训练|微调|finetune|fine-tune|更新参数)", text_low) is not None
    return td_is_base and ol_unknown and (hints or neg_train)


def _normalize_cognition_taxonomy(cog_items: List[Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for item_any in cog_items:
        if not isinstance(item_any, dict):
            continue
        item = item_any
        subsection = (item.get("subsection") or "").strip()
        if subsection == "Internalization: Cultivating Parametric Chemical Intuition" and _looks_training_free_internalization(
            item
        ):
            # training-free -> Externalization
            text_low = _join_item_text(item, ["summary", "training_data", "objective_or_loss", "signals_or_tools"])
            item["subsection"] = 'Externalization: Anchoring to Physical Reality via Interfacing'
            item["subsubsection"] = _externalization_subsubsection(text_low)
            out.append(item)
            continue

        if subsection == "Internalization: Cultivating Parametric Chemical Intuition":
            text_low = _join_item_text(item, ["summary", "training_data", "objective_or_loss", "signals_or_tools"])
            item["subsubsection"] = _internalization_stage(text_low)
        out.append(item)
    return out


def normalize_model_output(data: Any, bib_key: str, title: str, *, strict: bool = True) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("model output is not a JSON object")

    paper = data.get("paper")
    if not isinstance(paper, dict):
        paper = {}
        data["paper"] = paper
    paper["bib_key"] = bib_key
    paper["title"] = title
    paper.setdefault("method_name", "")

    rep = data.get("representation")
    if not isinstance(rep, list):
        rep = []
        data["representation"] = rep
    cog = data.get("cognition")
    if not isinstance(cog, list):
        cog = []
        data["cognition"] = cog
    app = data.get("application")
    if not isinstance(app, list):
        app = []
        data["application"] = app

    for item in rep:
        if not isinstance(item, dict):
            continue
        item.setdefault("details", [])
        item.setdefault("contributions", [])
        sub = (item.get("subsection") or "").strip()
        if sub not in REP_SUBSECTIONS:
            best, score = closest_choice(sub, REP_SUBSECTIONS.keys())
            if best:
                item["subsection"] = best
                sub = best
        subsubs_allowed = REP_SUBSECTIONS.get(sub, [])
        subsub = item.get("subsubsection")
        if isinstance(subsub, list):
            fixed: List[str] = []
            for s in subsub:
                s2 = str(s).strip()
                if s2 in subsubs_allowed:
                    fixed.append(s2)
                    continue
                best, score = closest_choice(s2, subsubs_allowed)
                if best and score >= 0.55:
                    fixed.append(best)
            item["subsubsection"] = fixed or (subsub if subsub else ["未明确"])
        else:
            s2 = str(subsub or "").strip()
            if not s2:
                item["subsubsection"] = "未明确"
            elif s2 not in subsubs_allowed:
                best, score = closest_choice(s2, subsubs_allowed)
                if best and score >= 0.55:
                    item["subsubsection"] = best
                else:
                    item["subsubsection"] = "未明确"

    for item in cog:
        if not isinstance(item, dict):
            continue
        item.setdefault("details", [])
        item.setdefault("contributions", [])
        item.setdefault("training_data", "未明确")
        item.setdefault("objective_or_loss", "未明确")
        item.setdefault("signals_or_tools", "无")
        sub = (item.get("subsection") or "").strip()
        if sub not in COG_SUBSECTIONS:
            best, score = closest_choice(sub, COG_SUBSECTIONS.keys())
            if best:
                item["subsection"] = best
                sub = best
        if sub not in COG_SUBSECTIONS:
            # infer subsection from subsubsection if possible
            raw_subsub = item.get("subsubsection")
            candidates: List[str] = []
            if isinstance(raw_subsub, list):
                candidates = [str(x).strip() for x in raw_subsub if str(x).strip()]
            else:
                s = str(raw_subsub or "").strip()
                if s:
                    candidates = [s]
            inferred = None
            for c in candidates:
                if c in COG_SUBSUB_TO_SUBSECTION:
                    inferred = COG_SUBSUB_TO_SUBSECTION[c]
                    break
            if inferred:
                item["subsection"] = inferred
                sub = inferred
        subsubs_allowed = COG_SUBSECTIONS.get(sub, [])
        subsub = item.get("subsubsection")
        if isinstance(subsub, list):
            fixed: List[str] = []
            for s in subsub:
                s2 = str(s).strip()
                if s2 in subsubs_allowed:
                    fixed.append(s2)
                    continue
                best, score = closest_choice(s2, subsubs_allowed)
                if best and score >= 0.55:
                    fixed.append(best)
                    continue
                # if subsub belongs to another cognition subsection, switch subsection
                mapped = COG_SUBSUB_TO_SUBSECTION.get(s2)
                if mapped and mapped != sub:
                    item["subsection"] = mapped
                    sub = mapped
                    subsubs_allowed = COG_SUBSECTIONS.get(sub, [])
                    if s2 in subsubs_allowed:
                        fixed.append(s2)
                else:
                    fixed.append("未明确")
            item["subsubsection"] = fixed or (subsub if subsub else ["未明确"])
        else:
            s2 = str(subsub or "").strip()
            if not s2:
                item["subsubsection"] = "未明确"
            elif s2 not in subsubs_allowed:
                best, score = closest_choice(s2, subsubs_allowed)
                if best and score >= 0.55:
                    item["subsubsection"] = best
                else:
                    mapped = COG_SUBSUB_TO_SUBSECTION.get(s2)
                    if mapped and mapped != sub:
                        item["subsection"] = mapped
                        sub = mapped
                        subsubs_allowed = COG_SUBSECTIONS.get(sub, [])
                        if s2 in subsubs_allowed:
                            item["subsubsection"] = s2
                        else:
                            item["subsubsection"] = "未明确"
                    else:
                        item["subsubsection"] = "未明确"

    # 强制对齐 cognition->Internalization 的三段式定义，并修正旧数据里“training-free 被塞进 Internalization”的情况
    data["cognition"] = _normalize_cognition_taxonomy(data.get("cognition", []) or [])

    for item in app:
        if not isinstance(item, dict):
            continue
        item.setdefault("datasets", [])
        item.setdefault("metrics_or_results", [])
        item.setdefault("scientific_findings", [])
        task = str(item.get("task") or "").strip()
        if task not in APP_TASKS:
            best, score = closest_choice(task, APP_TASKS)
            if best and score >= 0.55:
                item["task"] = best
            else:
                item["task"] = "Deciphering Hidden Properties via Discriminative Inference"

    if strict:
        # minimal validity checks (retryable)
        if not data.get("representation"):
            raise ValueError("missing representation entries")
        if not data.get("cognition"):
            raise ValueError("missing cognition entries")
        if not data.get("application"):
            raise ValueError("missing application entries")

    return data


def render_bullets(items: List[str], indent: int) -> List[str]:
    space = " " * indent
    return [f"{space}- {x}" for x in items if x]


def render_numbered(items: List[str], indent: int) -> List[str]:
    space = " " * indent
    out = []
    for i, x in enumerate([t for t in items if t], start=1):
        out.append(f"{space}{i}. {x}")
    return out


def render_paper_mindmap(data: Dict[str, Any]) -> str:
    paper = data.get("paper", {}) or {}
    bib_key = paper.get("bib_key", "") or ""
    title = paper.get("title", "") or ""
    method_name = paper.get("method_name", "") or ""

    lines: List[str] = []
    lines.append("<mindmap>")
    lines.append(f"## {bib_key} — {title}".strip(" —"))
    if method_name:
        lines.append(f"- Method/Framework: {method_name}")

    # Representation
    lines.append(f"- {REP_SECTION}")
    rep_items = data.get("representation", []) or []
    for subsection in REP_SUBSECTIONS.keys():
        subsection_items = [x for x in rep_items if (x.get("subsection") == subsection)]
        if not subsection_items:
            continue
        lines.append(f"    - {subsection}")
        for item in subsection_items:
            subsubs = item.get("subsubsection", "")
            if isinstance(subsubs, list):
                subsubs_list = [str(s).strip() for s in subsubs if str(s).strip()]
            else:
                subsubs_list = [str(subsubs).strip()] if str(subsubs).strip() else []
            if not subsubs_list:
                subsubs_list = ["未明确"]
            for subsub in subsubs_list:
                lines.append(f"        - {subsub}")
                summary = item.get("summary", "")
                if summary:
                    lines.append(f"            - Summary: {summary}")
                details = item.get("details", []) or []
                if details:
                    lines.append("            - Details:")
                    lines.extend(render_bullets(details, indent=16))
                contrib = item.get("contributions", []) or []
                if contrib:
                    lines.append("            - Contribution:")
                    lines.extend(render_numbered(contrib, indent=16))

    # Cognition
    lines.append(f"- {COG_SECTION}")
    cog_items = data.get("cognition", []) or []
    for subsection in COG_SUBSECTIONS.keys():
        subsection_items = [x for x in cog_items if (x.get("subsection") == subsection)]
        if not subsection_items:
            continue
        lines.append(f"    - {subsection}")
        for item in subsection_items:
            subsubs = item.get("subsubsection", "")
            if isinstance(subsubs, list):
                subsubs_list = [str(s).strip() for s in subsubs if str(s).strip()]
            else:
                subsubs_list = [str(subsubs).strip()] if str(subsubs).strip() else []
            if not subsubs_list:
                subsubs_list = ["未明确"]
            for subsub in subsubs_list:
                lines.append(f"        - {subsub}")
                summary = item.get("summary", "")
                if summary:
                    lines.append(f"            - Summary: {summary}")
                details = item.get("details", []) or []
                if details:
                    lines.append("            - Details:")
                    lines.extend(render_bullets(details, indent=16))
                contrib = item.get("contributions", []) or []
                if contrib:
                    lines.append("            - Contribution:")
                    lines.extend(render_numbered(contrib, indent=16))
                td = item.get("training_data", "")
                if td:
                    lines.append(f"            - Training data: {td}")
                ol = item.get("objective_or_loss", "")
                if ol:
                    lines.append(f"            - Objective/Loss: {ol}")
                st = item.get("signals_or_tools", "")
                if st:
                    lines.append(f"            - Signals/Tools: {st}")

    # Application
    lines.append(f"- {APP_SECTION}")
    app_items = data.get("application", []) or []
    for task in APP_TASKS:
        task_items = [x for x in app_items if (x.get("task") == task)]
        if not task_items:
            continue
        lines.append(f"    - {task}")
        for item in task_items:
            summary = item.get("summary", "")
            if summary:
                lines.append(f"        - Summary: {summary}")
            datasets = item.get("datasets", []) or []
            if datasets:
                lines.append("        - Datasets:")
                lines.extend(render_bullets(datasets, indent=12))
            metrics = item.get("metrics_or_results", []) or []
            if metrics:
                lines.append("        - Metrics/Results:")
                lines.extend(render_bullets(metrics, indent=12))
            findings = item.get("scientific_findings", []) or []
            if findings:
                lines.append("        - Scientific findings:")
                lines.extend(render_bullets(findings, indent=12))

    lines.append("</mindmap>")
    return "\n".join(lines).strip() + "\n"


def paper_id_from_meta(bib_key: str, paper_name: str) -> str:
    if bib_key:
        return safe_slug(bib_key)
    return safe_slug(paper_name)


def write_paper_outputs_to(
    data: Dict[str, Any], paper_id: str, *, json_dir: str, mindmap_dir: str
) -> Tuple[str, str]:
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(mindmap_dir, exist_ok=True)
    json_path = os.path.join(json_dir, f"{paper_id}.json")
    md_path = os.path.join(mindmap_dir, f"{paper_id}.md")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    mindmap = render_paper_mindmap(data)
    paper_title = (data.get("paper", {}) or {}).get("title", "") or ""
    paper_key = (data.get("paper", {}) or {}).get("bib_key", "") or ""
    with open(md_path, "w", encoding="utf-8") as f:
        if paper_key and paper_title:
            f.write(f"# {paper_key}: {paper_title}\n\n")
        elif paper_title:
            f.write(f"# {paper_title}\n\n")
        else:
            f.write(f"# {paper_id}\n\n")
        f.write(mindmap)

    return json_path, md_path


def write_paper_outputs(data: Dict[str, Any], paper_id: str) -> Tuple[str, str]:
    ensure_dirs()
    return write_paper_outputs_to(data, paper_id, json_dir=PAPER_JSON_DIR, mindmap_dir=PAPER_MINDMAP_DIR)


def iter_paper_json_files() -> Iterable[str]:
    if not os.path.exists(PAPER_JSON_DIR):
        return []
    for name in os.listdir(PAPER_JSON_DIR):
        if name.endswith(".json"):
            yield os.path.join(PAPER_JSON_DIR, name)


def iter_unrelated_json_files() -> Iterable[str]:
    if not os.path.exists(UNRELATED_JSON_DIR):
        return []
    for name in os.listdir(UNRELATED_JSON_DIR):
        if name.endswith(".json"):
            yield os.path.join(UNRELATED_JSON_DIR, name)


def fix_cognition_jsons(max_workers: int = DEFAULT_MAX_WORKERS, include_unrelated_dir: bool = False) -> None:
    """
    只基于规则/启发式修正现有 JSON 的 cognition 分类（不重新读PDF、不调用API）。
    """
    ensure_dirs()
    json_files = list(iter_paper_json_files())
    if include_unrelated_dir:
        json_files += list(iter_unrelated_json_files())

    print(f"待修正 cognition 的JSON数量: {len(json_files)} (include_unrelated={include_unrelated_dir})")
    if not json_files:
        return

    def worker(json_path: str) -> Dict[str, Any]:
        paper_id = os.path.splitext(os.path.basename(json_path))[0]
        in_unrelated = os.path.abspath(json_path).startswith(os.path.abspath(UNRELATED_JSON_DIR) + os.sep)
        out_json_dir = UNRELATED_JSON_DIR if in_unrelated else PAPER_JSON_DIR
        out_md_dir = UNRELATED_MINDMAP_DIR if in_unrelated else PAPER_MINDMAP_DIR
        try:
            data = load_json_maybe_dirty(json_path)
            paper = data.get("paper", {}) or {}
            bib_key = str(paper.get("bib_key", "") or "")
            title = str(paper.get("title", "") or "")
            if not title:
                title = paper_id.replace("_", " ")
            before = json.dumps(data.get("cognition", []), ensure_ascii=False, sort_keys=True)
            data2 = normalize_model_output(data, bib_key=bib_key, title=title, strict=False)
            after = json.dumps(data2.get("cognition", []), ensure_ascii=False, sort_keys=True)
            changed = before != after
            write_paper_outputs_to(data2, paper_id, json_dir=out_json_dir, mindmap_dir=out_md_dir)
            return {"status": "success", "paper_id": paper_id, "changed": changed, "dir": "unrelated" if in_unrelated else "paper_json"}
        except Exception as e:
            return {"status": "fail", "paper_id": paper_id, "error": str(e), "dir": "unrelated" if in_unrelated else "paper_json"}

    changed = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker, p): p for p in json_files}
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Fix cognition"):
            res = fut.result()
            if res.get("status") != "success":
                failed += 1
                print(f"\n失败: {res.get('paper_id')} - {res.get('error')}")
                continue
            if res.get("changed"):
                changed += 1

    print(f"\nFix cognition 完成: changed={changed}, failed={failed}, total={len(json_files)}")


def fix_jsons(max_workers: int = DEFAULT_MAX_WORKERS, include_unrelated_dir: bool = False) -> None:
    """
    只基于本地 normalize 规则修正现有 JSON（不重新读PDF、不调用API）。
    用于清理模型偶发输出的“错用subsection/subsubsection字符串”等问题。
    """
    ensure_dirs()
    json_files = list(iter_paper_json_files())
    if include_unrelated_dir:
        json_files += list(iter_unrelated_json_files())

    print(f"待修正 JSON 数量: {len(json_files)} (include_unrelated={include_unrelated_dir})")
    if not json_files:
        return

    def worker(json_path: str) -> Dict[str, Any]:
        paper_id = os.path.splitext(os.path.basename(json_path))[0]
        in_unrelated = os.path.abspath(json_path).startswith(os.path.abspath(UNRELATED_JSON_DIR) + os.sep)
        out_json_dir = UNRELATED_JSON_DIR if in_unrelated else PAPER_JSON_DIR
        out_md_dir = UNRELATED_MINDMAP_DIR if in_unrelated else PAPER_MINDMAP_DIR
        try:
            data = load_json_maybe_dirty(json_path)
            paper = data.get("paper", {}) or {}
            bib_key = str(paper.get("bib_key", "") or "")
            title = str(paper.get("title", "") or "")
            if not title:
                title = paper_id.replace("_", " ")
            before = json.dumps(
                {
                    "representation": data.get("representation", []),
                    "cognition": data.get("cognition", []),
                    "application": data.get("application", []),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            data2 = normalize_model_output(data, bib_key=bib_key, title=title, strict=False)
            after = json.dumps(
                {
                    "representation": data2.get("representation", []),
                    "cognition": data2.get("cognition", []),
                    "application": data2.get("application", []),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            changed = before != after
            write_paper_outputs_to(data2, paper_id, json_dir=out_json_dir, mindmap_dir=out_md_dir)
            return {
                "status": "success",
                "paper_id": paper_id,
                "changed": changed,
                "dir": "unrelated" if in_unrelated else "paper_json",
            }
        except Exception as e:
            return {
                "status": "fail",
                "paper_id": paper_id,
                "error": str(e),
                "dir": "unrelated" if in_unrelated else "paper_json",
            }

    changed = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker, p): p for p in json_files}
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Fix json"):
            res = fut.result()
            if res.get("status") != "success":
                failed += 1
                print(f"\n失败: {res.get('paper_id')} - {res.get('error')}")
                continue
            if res.get("changed"):
                changed += 1

    print(f"\nFix json 完成: changed={changed}, failed={failed}, total={len(json_files)}")


def merge_by_subsubsection() -> List[str]:
    """
    将所有 paper_json 聚合成“按 subsubsection 拆分”的 mindmap 文件。
    返回生成的文件路径列表。
    """
    ensure_dirs()
    # 清空旧的聚合输出，避免过滤前的“残留文件”混入结果
    if os.path.exists(SUBSUBSECTION_DIR):
        shutil.rmtree(SUBSUBSECTION_DIR)
    os.makedirs(SUBSUBSECTION_DIR, exist_ok=True)
    by_key: Dict[Tuple[str, str, str], Dict[str, List[Dict[str, Any]]]] = {}
    # key: (section, subsection, subsub_or_task) -> {paper_id: [entry_dicts...]}

    records: List[Tuple[str, str, str, str, Dict[str, Any]]] = []
    for path in iter_paper_json_files():
        data = load_json_maybe_dirty(path)
        paper = data.get("paper", {}) or {}
        paper_id = os.path.splitext(os.path.basename(path))[0]
        bib_key = paper.get("bib_key", "") or ""
        title = paper.get("title", "") or ""
        title_norm = normalize_for_match(title)
        records.append((paper_id, bib_key, title, title_norm, data))

    bib_norms: List[str] = [t_norm for _, bk, _, t_norm, _ in records if bk and t_norm]

    def is_duplicate_without_bib(title_norm: str) -> bool:
        if not title_norm or not bib_norms:
            return False
        best = 0.0
        for bn in bib_norms:
            score = score_title_match(title_norm, bn)
            if score > best:
                best = score
        return best >= 0.86

    for paper_id, bib_key, title, title_norm, data in records:
        if not bib_key and is_duplicate_without_bib(title_norm):
            # 已有bib_key版本，跳过旧的/无key版本，避免同一论文重复出现在聚合图里
            continue

        # Representation entries
        for item in data.get("representation", []) or []:
            subsection = item.get("subsection", "")
            subsubs = item.get("subsubsection", "")
            if isinstance(subsubs, list):
                subsub_list = [str(s).strip() for s in subsubs if str(s).strip()]
            else:
                subsub_list = [str(subsubs).strip()] if str(subsubs).strip() else []
            for subsub in subsub_list:
                if not subsection or not subsub or subsub == "未明确":
                    continue
                k = ("Representation", subsection, subsub)
                by_key.setdefault(k, {}).setdefault(paper_id, []).append(
                    {"bib_key": bib_key, "title": title, "entry": item}
                )

        # Cognition entries
        for item in data.get("cognition", []) or []:
            subsection = item.get("subsection", "")
            subsubs = item.get("subsubsection", "")
            if isinstance(subsubs, list):
                subsub_list = [str(s).strip() for s in subsubs if str(s).strip()]
            else:
                subsub_list = [str(subsubs).strip()] if str(subsubs).strip() else []
            for subsub in subsub_list:
                if not subsection or not subsub or subsub == "未明确":
                    continue
                k = ("Cognition", subsection, subsub)
                by_key.setdefault(k, {}).setdefault(paper_id, []).append(
                    {"bib_key": bib_key, "title": title, "entry": item}
                )

        # Application entries (task作为“subsubsection”文件)
        for item in data.get("application", []) or []:
            task = item.get("task", "")
            if not task:
                continue
            k = ("Application", "Application", task)
            by_key.setdefault(k, {}).setdefault(paper_id, []).append(
                {"bib_key": bib_key, "title": title, "entry": item}
            )

    written: List[str] = []
    for (section, subsection, subsub), papers in by_key.items():
        if not papers:
            continue

        if section == "Application":
            out_dir = os.path.join(SUBSUBSECTION_DIR, "Application")
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f"{safe_slug(subsub)}.md")
            root = subsub
        else:
            out_dir = os.path.join(SUBSUBSECTION_DIR, safe_slug(section), safe_slug(subsection))
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f"{safe_slug(subsub)}.md")
            root = subsub

        lines: List[str] = []
        lines.append(f"# {section} / {subsection} / {subsub}\n")
        lines.append("<mindmap>")
        lines.append(f"## {root}")

        # stable order: by bib_key then title then paper_id
        def sort_key(pid: str) -> Tuple[str, str, str]:
            items = papers.get(pid, [])
            if items:
                bk = items[0].get("bib_key", "") or ""
                tt = items[0].get("title", "") or ""
            else:
                bk, tt = "", ""
            return (bk, tt, pid)

        for pid in sorted(papers.keys(), key=sort_key):
            items = papers[pid]
            if not items:
                continue
            bib_key = items[0].get("bib_key", "") or ""
            title = items[0].get("title", "") or ""
            cite_key = bib_key or pid
            display_title = title or pid
            lines.append(f"- {display_title}")
            lines.append(f"    - BibTeXKey: {cite_key}")

            for it in items:
                entry = it.get("entry", {}) or {}
                summary = entry.get("summary", "")
                if summary:
                    lines.append(f"    - Summary: {summary}")
                details = entry.get("details", []) or []
                if details:
                    lines.append("    - Details:")
                    lines.extend(render_bullets(details, indent=8))

                if section == "Representation":
                    contrib = entry.get("contributions", []) or []
                    if contrib:
                        lines.append("    - Contribution:")
                        lines.extend(render_numbered(contrib, indent=8))

                if section == "Cognition":
                    contrib = entry.get("contributions", []) or []
                    if contrib:
                        lines.append("    - Contribution:")
                        lines.extend(render_numbered(contrib, indent=8))
                    td = entry.get("training_data", "")
                    if td:
                        lines.append(f"    - Training data: {td}")
                    ol = entry.get("objective_or_loss", "")
                    if ol:
                        lines.append(f"    - Objective/Loss: {ol}")
                    st = entry.get("signals_or_tools", "")
                    if st:
                        lines.append(f"    - Signals/Tools: {st}")

                if section == "Application":
                    datasets = entry.get("datasets", []) or []
                    if datasets:
                        lines.append("    - Datasets:")
                        lines.extend(render_bullets(datasets, indent=8))
                    metrics = entry.get("metrics_or_results", []) or []
                    if metrics:
                        lines.append("    - Metrics/Results:")
                        lines.extend(render_bullets(metrics, indent=8))
                    findings = entry.get("scientific_findings", []) or []
                    if findings:
                        lines.append("    - Scientific findings:")
                        lines.extend(render_bullets(findings, indent=8))

        lines.append("</mindmap>")
        content = "\n".join(lines).strip() + "\n"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        written.append(out_path)

    return written


def summarize_for_topic_check(data: Dict[str, Any]) -> Dict[str, Any]:
    paper = data.get("paper", {}) or {}
    def clip_list(xs: Any, max_n: int) -> List[Any]:
        if not isinstance(xs, list):
            return []
        return xs[:max_n]

    rep = []
    for item in clip_list(data.get("representation", []), 4):
        if not isinstance(item, dict):
            continue
        rep.append(
            {
                "subsection": item.get("subsection", ""),
                "subsubsection": item.get("subsubsection", ""),
                "summary": item.get("summary", ""),
            }
        )

    cog = []
    for item in clip_list(data.get("cognition", []), 6):
        if not isinstance(item, dict):
            continue
        cog.append(
            {
                "subsection": item.get("subsection", ""),
                "subsubsection": item.get("subsubsection", ""),
                "summary": item.get("summary", ""),
            }
        )

    app = []
    for item in clip_list(data.get("application", []), 6):
        if not isinstance(item, dict):
            continue
        app.append({"task": item.get("task", ""), "summary": item.get("summary", "")})

    return {
        "paper": {
            "bib_key": paper.get("bib_key", ""),
            "title": paper.get("title", ""),
            "method_name": paper.get("method_name", ""),
        },
        "representation": rep,
        "cognition": cog,
        "application": app,
    }


def topic_check_with_api(
    client: OpenAI, summary_obj: Dict[str, Any], max_retries: int = DEFAULT_MAX_RETRIES
) -> Dict[str, Any]:
    paper = summary_obj.get("paper", {}) or {}
    title = str(paper.get("title", "") or "")
    method_name = str(paper.get("method_name", "") or "")
    rep = summary_obj.get("representation", []) or []
    cog = summary_obj.get("cognition", []) or []
    app = summary_obj.get("application", []) or []

    # 拼成一个“证据可引用”的输入文本，要求模型从中抽取 evidence（精确子串）
    input_lines = [
        f"TITLE: {title}",
        f"METHOD: {method_name}",
        "REP:",
    ]
    for x in rep:
        if isinstance(x, dict):
            input_lines.append(f"- {x.get('subsubsection','')}: {x.get('summary','')}")
    input_lines.append("COG:")
    for x in cog:
        if isinstance(x, dict):
            input_lines.append(f"- {x.get('subsubsection','')}: {x.get('summary','')}")
    input_lines.append("APP:")
    for x in app:
        if isinstance(x, dict):
            input_lines.append(f"- {x.get('task','')}: {x.get('summary','')}")
    input_text = "\n".join([ln for ln in input_lines if ln is not None]).strip()

    prompt = f"""你是一个严格的“论文相关性判定器”。我在写一篇关于【分子/化学领域的分子表示与分子LLM/生成/推理】的综述。

判定目标：这篇论文是否与“分子/化学（以小分子、化学反应、药物发现、分子性质、分子生成、计算化学、材料化学）”主题相关？

判定规则（务必遵循）：
- related=true：主要研究对象或任务属于小分子/化学反应/药物发现/分子性质/分子生成/合成规划/计算化学/材料化学；蛋白/口袋/受体相关也可算 related，但必须服务于小分子化学/药物发现（例如口袋条件生成、对接打分、蛋白-配体结合等）。
- related=false：主要是基因组/转录组/单细胞/细胞图谱/疾病影像诊断/纯NLP/纯视觉/通用AI agent/HPC连接等，与化学分子任务无关或只是泛泛提及。

重要约束（防止幻觉）：
1) 你只能依据下方“INPUT”里的内容判断，不允许引入任何外部信息
2) 你的 reason 必须引用 INPUT 中出现的关键词，不要编造不相关领域（如高能物理/引力波等）
3) 你必须给出 evidence: 1-3 个【从 INPUT 中原样复制】的短语（精确子串），用于支撑判定

INPUT（请只依据这里的内容）：
{input_text}

只输出 JSON，用 <json>...</json> 包裹：
<json>
{{
  "related": true,
  "confidence": 0.0,
  "primary_domain": "chemistry_molecule|biology_genomics|cell_biology|medical_imaging|general_ai|other",
  "reason": "一句话中文理由（必须基于evidence）",
  "evidence": ["从INPUT中复制的短语1", "短语2"]
}}
</json>
"""

    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你只做领域相关性判定，输出严格JSON。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=600,
            )
            content = resp.choices[0].message.content or ""
            json_block = extract_json_block(content)
            out = json.loads(json_block)
            out = validate_topic_check_output(out, input_text=input_text)
            if not isinstance(out, dict) or "related" not in out:
                raise ValueError("invalid topic-check output")
            out["_usage"] = {
                "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
                "completion_tokens": getattr(resp.usage, "completion_tokens", None),
                "total_tokens": getattr(resp.usage, "total_tokens", None),
            }
            return out
        except Exception as e:
            last_exc = e
            if attempt >= max_retries - 1:
                if isinstance(e, ValueError) and "evidence" in str(e).lower():
                    fallback = heuristic_topic_check(summary_obj)
                    fallback["_fallback"] = "heuristic_due_to_evidence"
                    return fallback
                raise
            if not is_retryable_exception(e):
                raise
            delay = min(45.0, (1.6**attempt) + random.uniform(0.0, 0.8))
            time.sleep(delay)
    raise RuntimeError(f"topic-check retries exhausted: {last_exc}")


def heuristic_topic_check(summary_obj: Dict[str, Any]) -> Dict[str, Any]:
    paper = summary_obj.get("paper", {}) or {}
    title = str(paper.get("title", "") or "")
    method = str(paper.get("method_name", "") or "")

    rep_text = " ".join([str(x.get("summary", "") or "") for x in summary_obj.get("representation", []) or [] if isinstance(x, dict)])
    cog_text = " ".join([str(x.get("summary", "") or "") for x in summary_obj.get("cognition", []) or [] if isinstance(x, dict)])
    app_text = " ".join([str(x.get("summary", "") or "") for x in summary_obj.get("application", []) or [] if isinstance(x, dict)])
    text = " ".join([title, method, rep_text, cog_text, app_text])
    text_norm = normalize_for_match(text)

    pos = [
        "molecule",
        "molecular",
        "chem",
        "chemistry",
        "smiles",
        "selfies",
        "iupac",
        "drug",
        "ligand",
        "reaction",
        "retrosynthesis",
        "synthesis",
        "docking",
        "binding affinity",
        "protein ligand",
        "pocket",
        "conformer",
        "admet",
        "qed",
        "lipinski",
        "tox",
        "cheminformatics",
        "catalyst",
        "catalysis",
        "material",
        "crystal",
        "polymer",
    ]
    neg = [
        "genome",
        "genomic",
        "dna",
        "transcript",
        "transcriptome",
        "single cell",
        "cell atlas",
        "cellular",
        "pathology",
        "radiology",
        "mri",
        "ct",
        "histopathology",
        "glioma",
        "oncology",
    ]

    pos_hit = any(k in text_norm for k in pos)
    neg_hit = any(k in text_norm for k in neg)

    if pos_hit and not (("dna" in text_norm or "genome" in text_norm) and not ("molecule" in text_norm or "smiles" in text_norm)):
        return {
            "related": True,
            "confidence": 0.55,
            "primary_domain": "chemistry_molecule",
            "reason": "标题/摘要中包含分子/化学相关关键词（如molecule/SMILES/docking/reaction等），判定为相关。",
            "evidence": [title] if title else [],
        }
    if neg_hit and not pos_hit:
        return {
            "related": False,
            "confidence": 0.55,
            "primary_domain": "biology_genomics" if ("genome" in text_norm or "dna" in text_norm) else "other",
            "reason": "标题/摘要中主要出现基因组/细胞/病理等关键词且缺少分子化学任务信号，判定为不相关。",
            "evidence": [title] if title else [],
        }
    # default conservative
    return {
        "related": True,
        "confidence": 0.51,
        "primary_domain": "chemistry_molecule",
        "reason": "信息不足以可靠排除分子/化学任务，暂保留为相关（建议人工抽查）。",
        "evidence": [title] if title else [],
    }


def validate_topic_check_output(out: Any, input_text: str) -> Dict[str, Any]:
    if not isinstance(out, dict):
        raise ValueError("topic-check output is not an object")

    related = out.get("related")
    if isinstance(related, str):
        related = related.strip().lower()
        if related in {"true", "yes", "1"}:
            out["related"] = True
        elif related in {"false", "no", "0"}:
            out["related"] = False
        else:
            raise ValueError("invalid related value")
    elif isinstance(related, bool):
        out["related"] = related
    else:
        raise ValueError("invalid related type")

    confidence = out.get("confidence")
    try:
        out["confidence"] = float(confidence)
    except Exception:
        out["confidence"] = 0.0
    out["confidence"] = max(0.0, min(1.0, out["confidence"]))

    primary_domain = str(out.get("primary_domain") or "").strip()
    allowed = {"chemistry_molecule", "biology_genomics", "cell_biology", "medical_imaging", "general_ai", "other"}
    if primary_domain not in allowed:
        out["primary_domain"] = "other"

    reason = str(out.get("reason") or "").strip()
    if not reason:
        raise ValueError("missing reason")
    out["reason"] = reason

    evidence = out.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("missing evidence")
    ev_fixed: List[str] = []
    for e in evidence[:3]:
        s = str(e or "").strip()
        s = s.strip(" \"'`")
        if s.startswith("- "):
            s = s[2:].strip()
        if not s:
            continue
        if not evidence_matches_input(s, input_text):
            raise ValueError("evidence not found in input")
        ev_fixed.append(s)
    if not ev_fixed:
        raise ValueError("empty evidence")
    out["evidence"] = ev_fixed
    return out


def evidence_matches_input(evidence: str, input_text: str) -> bool:
    if not evidence or not input_text:
        return False
    if evidence in input_text:
        return True
    ev_norm = normalize_for_match(evidence)
    in_norm = normalize_for_match(input_text)
    if not ev_norm or not in_norm:
        return False
    if ev_norm in in_norm:
        return True
    ev_tokens = set(ev_norm.split())
    in_tokens = set(in_norm.split())
    if ev_tokens and ev_tokens.issubset(in_tokens):
        return True
    # very light fuzzy fallback (avoid false positives on unrelated domains)
    return score_title_match(ev_norm, in_norm) >= 0.70


def append_jsonl(path: str, obj: Dict[str, Any], lock: threading.Lock) -> None:
    line = json.dumps(obj, ensure_ascii=False)
    with lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def safe_move(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(src):
        return
    # overwrite destination to keep latest reruns consistent
    os.replace(src, dst)


def filter_unrelated_jsons(
    max_workers: int = DEFAULT_MAX_WORKERS,
    per_key_concurrency: Optional[int] = None,
    max_retries: int = DEFAULT_MAX_RETRIES,
    include_unrelated_dir: bool = False,
    only_paper_id: Optional[str] = None,
) -> Dict[str, int]:
    """
    对每个 paper_json 调用 API 判定是否与“分子/化学（小分子/反应/药物发现等）”相关。
    unrelated 的会移动到 mindmap_v2/unrelated/ 下。
    """
    ensure_dirs()
    api_keys = load_api_keys()
    if not api_keys:
        raise RuntimeError(f"No API keys found in {API_KEYS_FILE}")

    json_files = list(iter_paper_json_files())
    if include_unrelated_dir:
        json_files += list(iter_unrelated_json_files())

    if only_paper_id:
        pid = only_paper_id.strip()
        if not pid.endswith(".json"):
            pid = pid + ".json"
        picked = [p for p in json_files if os.path.basename(p) == pid]
        if not picked:
            raise FileNotFoundError(f"paper_id not found in paper_json/unrelated: {only_paper_id}")
        json_files = picked

    if per_key_concurrency is None:
        per_key_concurrency = max(1, min(DEFAULT_PER_KEY_CONCURRENCY_CAP, max_workers // max(1, len(api_keys))))
    key_semaphores: Dict[str, threading.Semaphore] = {k: threading.Semaphore(per_key_concurrency) for k in api_keys}
    log_lock = threading.Lock()
    run_id = time.strftime("%Y%m%d_%H%M%S")

    print(f"待判定JSON数量: {len(json_files)}")
    print(f"使用 {max_workers} 线程; per-key concurrency={per_key_concurrency}; retries={max_retries}")

    def worker(task: Tuple[str, str, int]) -> Dict[str, Any]:
        json_path, api_key, idx = task
        paper_id = os.path.splitext(os.path.basename(json_path))[0]
        in_unrelated = os.path.abspath(json_path).startswith(os.path.abspath(UNRELATED_JSON_DIR) + os.sep)
        data = load_json_maybe_dirty(json_path)
        summary_obj = summarize_for_topic_check(data)
        client = create_client(api_key)
        sem = key_semaphores[api_key]
        with sem:
            verdict = topic_check_with_api(client, summary_obj, max_retries=max_retries)

        related = bool(verdict.get("related"))
        confidence = verdict.get("confidence", None)
        primary_domain = verdict.get("primary_domain", "")
        reason = verdict.get("reason", "")

        log_obj = {
            "run_id": run_id,
            "paper_id": paper_id,
            "bib_key": (summary_obj.get("paper", {}) or {}).get("bib_key", ""),
            "title": (summary_obj.get("paper", {}) or {}).get("title", ""),
            "related": related,
            "confidence": confidence,
            "primary_domain": primary_domain,
            "reason": reason,
            "evidence": verdict.get("evidence", []),
            "source_dir": "unrelated" if in_unrelated else "paper_json",
            "usage": verdict.get("_usage", {}),
            "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        append_jsonl(TOPIC_FILTER_LOG, log_obj, lock=log_lock)

        if related:
            if in_unrelated:
                # move back to main
                safe_move(json_path, os.path.join(PAPER_JSON_DIR, os.path.basename(json_path)))
                safe_move(
                    os.path.join(UNRELATED_MINDMAP_DIR, f"{paper_id}.md"),
                    os.path.join(PAPER_MINDMAP_DIR, f"{paper_id}.md"),
                )
                return {"status": "moved_back", "paper_id": paper_id}
            return {"status": "related", "paper_id": paper_id}

        # unrelated
        if in_unrelated:
            return {"status": "unrelated", "paper_id": paper_id}

        safe_move(json_path, os.path.join(UNRELATED_JSON_DIR, os.path.basename(json_path)))
        safe_move(
            os.path.join(PAPER_MINDMAP_DIR, f"{paper_id}.md"),
            os.path.join(UNRELATED_MINDMAP_DIR, f"{paper_id}.md"),
        )
        return {"status": "moved_out", "paper_id": paper_id}

    tasks: List[Tuple[str, str, int]] = [
        (p, api_keys[i % len(api_keys)], i) for i, p in enumerate(sorted(json_files))
    ]

    counts = {"related": 0, "unrelated": 0, "moved_out": 0, "moved_back": 0, "failed": 0}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker, t): t for t in tasks}
        for fut in tqdm(as_completed(futures), total=len(futures), desc="Topic过滤"):
            try:
                res = fut.result()
                if res["status"] == "related":
                    counts["related"] += 1
                elif res["status"] == "unrelated":
                    counts["unrelated"] += 1
                else:
                    counts[res["status"]] += 1
            except Exception as e:
                counts["failed"] += 1
                t = futures.get(fut)
                if t:
                    print(f"\n判定失败: {os.path.basename(t[0])} - {e}")
                else:
                    print(f"\n判定失败: {e}")

    print(
        f"\nTopic过滤完成: related={counts['related']}, unrelated={counts['unrelated']}, "
        f"moved_out={counts['moved_out']}, moved_back={counts['moved_back']}, failed={counts['failed']}"
    )
    print(f"Log: {TOPIC_FILTER_LOG}")
    return counts


def get_all_pdfs() -> List[str]:
    pdf_files: List[str] = []
    for pdf_dir in PDF_DIRS:
        if os.path.exists(pdf_dir):
            for f in os.listdir(pdf_dir):
                if f.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(pdf_dir, f))
    return sorted(pdf_files)


def choose_default_test_pdf() -> Optional[str]:
    for pdf in get_all_pdfs():
        try:
            size = os.path.getsize(pdf)
        except OSError:
            continue
        if 500000 < size < 3000000:
            return pdf
    all_pdfs = get_all_pdfs()
    return all_pdfs[0] if all_pdfs else None


def analyze_single_pdf(pdf_path: str, api_key: str, bib_entries: List[BibEntry]) -> Dict[str, Any]:
    paper_name = os.path.basename(pdf_path).replace(".pdf", "")
    matched, score = match_bib_by_title(paper_name, bib_entries)
    if matched and score >= 0.58:
        bib_key = matched.key
        title = matched.title_clean or paper_name.replace("_", " ")
    else:
        bib_key = ""
        title = paper_name.replace("_", " ")

    paper_text = extract_text_from_pdf(pdf_path)
    if paper_text.startswith("Error"):
        raise RuntimeError(paper_text)

    client = create_client(api_key)
    return analyze_paper_with_retries(client, paper_text, bib_key=bib_key, title=title)


def is_retryable_exception(exc: Exception) -> bool:
    if isinstance(exc, (RateLimitError, APITimeoutError, APIConnectionError)):
        return True
    if isinstance(exc, APIStatusError):
        status = getattr(exc, "status_code", None)
        if status is None:
            return True
        return int(status) >= 500 or int(status) == 429
    if isinstance(exc, APIError):
        return True
    if isinstance(exc, json.JSONDecodeError):
        return True
    if isinstance(exc, ValueError):
        # 用于触发“缺少必要字段”等质量问题的重试
        return True
    msg = str(exc).lower()
    return any(k in msg for k in ["rate", "429", "timeout", "timed out", "connection", "502", "503", "504"])


def analyze_paper_with_retries(
    client: OpenAI,
    paper_text: str,
    bib_key: str,
    title: str,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> Dict[str, Any]:
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            return analyze_paper(client, paper_text, bib_key=bib_key, title=title)
        except Exception as e:
            last_exc = e
            if not is_retryable_exception(e) or attempt >= max_retries - 1:
                raise
            # exponential backoff with jitter
            delay = min(60.0, (1.6**attempt) + random.uniform(0.0, 0.8))
            time.sleep(delay)
    raise RuntimeError(f"retries exhausted: {last_exc}")


def test_single_pdf(pdf_path: Optional[str] = None, bib_path: str = BIB_FILE) -> Dict[str, Any]:
    ensure_dirs()
    api_keys = load_api_keys()
    if not api_keys:
        raise RuntimeError(f"No API keys found in {API_KEYS_FILE}")
    if pdf_path is None:
        pdf_path = choose_default_test_pdf()
    if not pdf_path:
        raise RuntimeError("No PDF found.")

    bib_entries = parse_bibtex_file(bib_path)

    print(f"测试PDF: {pdf_path}")
    print(f"文件大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
    print(f"Bib entries loaded: {len(bib_entries)}")

    start = time.time()
    data = analyze_single_pdf(pdf_path, api_keys[0], bib_entries)
    elapsed = time.time() - start

    paper = data.get("paper", {}) or {}
    paper_id = paper_id_from_meta(paper.get("bib_key", "") or "", os.path.basename(pdf_path).replace(".pdf", ""))
    json_path, md_path = write_paper_outputs(data, paper_id)
    print(f"\n✅ 完成 (用时 {elapsed:.2f}s)")
    print(f"- paper json: {json_path}")
    print(f"- paper mindmap: {md_path}")
    print(f"- usage: {data.get('_usage')}")
    return data


def process_single_pdf_worker(
    args: Tuple[str, List[str], int, bool, str, List[BibEntry], Dict[str, threading.Semaphore], int]
) -> Dict[str, Any]:
    pdf_path, api_keys, key_index, skip_existing, bib_path, bib_entries, key_semaphores, max_retries = args
    paper_name = os.path.basename(pdf_path).replace(".pdf", "")

    matched, score = match_bib_by_title(paper_name, bib_entries)
    if matched and score >= 0.58:
        bib_key = matched.key
        title = matched.title_clean or paper_name.replace("_", " ")
    else:
        bib_key = ""
        title = paper_name.replace("_", " ")

    paper_id = paper_id_from_meta(bib_key, paper_name)
    json_path = os.path.join(PAPER_JSON_DIR, f"{paper_id}.json")
    if skip_existing and os.path.exists(json_path):
        return {"status": "skipped", "paper_id": paper_id, "paper_name": paper_name}

    paper_text = extract_text_from_pdf(pdf_path)
    if paper_text.startswith("Error"):
        return {"status": "fail", "paper_id": paper_id, "paper_name": paper_name, "error": paper_text}

    api_key = api_keys[key_index % len(api_keys)]
    client = create_client(api_key)
    try:
        sem = key_semaphores.get(api_key)
        if sem is None:
            data = analyze_paper_with_retries(client, paper_text, bib_key=bib_key, title=title, max_retries=max_retries)
        else:
            with sem:
                data = analyze_paper_with_retries(
                    client, paper_text, bib_key=bib_key, title=title, max_retries=max_retries
                )
        write_paper_outputs(data, paper_id)
        return {"status": "success", "paper_id": paper_id, "paper_name": paper_name}
    except Exception as e:
        return {"status": "fail", "paper_id": paper_id, "paper_name": paper_name, "error": str(e)}


def batch_process_pdfs(
    max_papers: Optional[int] = None,
    skip_existing: bool = True,
    max_workers: int = DEFAULT_MAX_WORKERS,
    bib_path: str = BIB_FILE,
    per_key_concurrency: Optional[int] = None,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> None:
    ensure_dirs()
    api_keys = load_api_keys()
    if not api_keys:
        raise RuntimeError(f"No API keys found in {API_KEYS_FILE}")

    bib_entries = parse_bibtex_file(bib_path)
    all_pdfs = get_all_pdfs()
    if max_papers:
        all_pdfs = all_pdfs[:max_papers]

    print(f"共找到 {len(all_pdfs)} 个PDF文件")
    print(f"使用 {max_workers} 个线程并行处理")
    print(f"Bib entries loaded: {len(bib_entries)}")

    if per_key_concurrency is None:
        per_key_concurrency = max(1, min(DEFAULT_PER_KEY_CONCURRENCY_CAP, max_workers // max(1, len(api_keys))))
    key_semaphores: Dict[str, threading.Semaphore] = {
        k: threading.Semaphore(per_key_concurrency) for k in api_keys
    }
    print(f"Per-key concurrency: {per_key_concurrency} (keys={len(api_keys)})")
    print(f"Max retries per paper: {max_retries}")

    tasks = [
        (pdf, api_keys, i, skip_existing, bib_path, bib_entries, key_semaphores, max_retries)
        for i, pdf in enumerate(all_pdfs)
    ]

    success = 0
    skipped = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_pdf_worker, t): t for t in tasks}
        for fut in tqdm(as_completed(futures), total=len(futures), desc="处理PDF"):
            try:
                res = fut.result()
            except Exception as e:
                failed += 1
                print(f"\n异常: {e}")
                continue

            if res["status"] == "success":
                success += 1
            elif res["status"] == "skipped":
                skipped += 1
            else:
                failed += 1
                print(f"\n失败: {res.get('paper_name')} - {res.get('error')}")

    print(f"\n处理完成! 成功: {success}, 跳过: {skipped}, 失败: {failed}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="使用 DeepSeek API 阅读PDF论文并生成Survey思维导图（v2）")
    parser.add_argument("--test", action="store_true", help="测试单个PDF")
    parser.add_argument("--pdf", type=str, help="指定要测试的PDF路径")
    parser.add_argument("--batch", action="store_true", help="批量处理所有PDF")
    parser.add_argument("--max", type=int, default=None, help="最多处理的论文数量")
    parser.add_argument("--workers", type=int, default=DEFAULT_MAX_WORKERS, help=f"并行线程数 (默认{DEFAULT_MAX_WORKERS})")
    parser.add_argument("--force", action="store_true", help="强制覆盖已存在的paper_json")
    parser.add_argument("--merge", action="store_true", help="按subsubsection聚合输出思维导图")
    parser.add_argument("--filter-unrelated", action="store_true", help="调用API过滤不相关论文(JSON)，移动到unrelated/")
    parser.add_argument("--include-unrelated", action="store_true", help="过滤时也重新检查 unrelated/ 下的JSON（可自动移回）")
    parser.add_argument("--filter-one", type=str, default=None, help="只过滤单个paper_id(或paper_id.json)，用于增量修复")
    parser.add_argument("--fix-cognition", action="store_true", help="修正现有JSON的cognition三段式分类（不调用API）")
    parser.add_argument("--fix-json", action="store_true", help="修正现有JSON的taxonomy字段（不调用API）")
    parser.add_argument("--bib", type=str, default=BIB_FILE, help="ref.bib路径")
    parser.add_argument("--api-keys", type=str, default=API_KEYS_FILE, help="API keys文件路径")
    parser.add_argument("--pdf-dirs", nargs='+', default=PDF_DIRS, help="PDF目录列表")
    parser.add_argument("--output", type=str, default=OUTPUT_ROOT, help="输出根目录")
    parser.add_argument("--per-key", type=int, default=None, help="每个API key的并发上限(默认自动推断)")
    parser.add_argument("--retries", type=int, default=DEFAULT_MAX_RETRIES, help=f"每篇论文最大重试次数(默认{DEFAULT_MAX_RETRIES})")

    args = parser.parse_args()

    # Update global paths from command line arguments
    API_KEYS_FILE = args.api_keys
    BIB_FILE = args.bib
    PDF_DIRS = args.pdf_dirs
    OUTPUT_ROOT = args.output
    PAPER_JSON_DIR = os.path.join(OUTPUT_ROOT, "paper_json")
    PAPER_MINDMAP_DIR = os.path.join(OUTPUT_ROOT, "paper_mindmaps")
    SUBSUBSECTION_DIR = os.path.join(OUTPUT_ROOT, "by_subsubsection")
    UNRELATED_ROOT = os.path.join(OUTPUT_ROOT, "unrelated")
    UNRELATED_JSON_DIR = os.path.join(UNRELATED_ROOT, "paper_json")
    UNRELATED_MINDMAP_DIR = os.path.join(UNRELATED_ROOT, "paper_mindmaps")
    TOPIC_FILTER_LOG = os.path.join(OUTPUT_ROOT, "topic_filter_results.jsonl")

    if args.filter_one:
        filter_unrelated_jsons(
            max_workers=min(args.workers, 8),
            per_key_concurrency=args.per_key,
            max_retries=args.retries,
            include_unrelated_dir=True,
            only_paper_id=args.filter_one,
        )
    elif args.fix_json:
        fix_jsons(max_workers=args.workers, include_unrelated_dir=args.include_unrelated)
    elif args.fix_cognition:
        fix_cognition_jsons(max_workers=args.workers, include_unrelated_dir=args.include_unrelated)
    elif args.filter_unrelated:
        filter_unrelated_jsons(
            max_workers=args.workers,
            per_key_concurrency=args.per_key,
            max_retries=args.retries,
            include_unrelated_dir=args.include_unrelated,
        )
    elif args.merge:
        written = merge_by_subsubsection()
        print(f"✅ 生成 {len(written)} 个按subsubsection聚合的mindmap文件")
        for p in sorted(written)[:20]:
            print(f"- {p}")
        if len(written) > 20:
            print(f"...(共{len(written)}个，仅展示前20个)")
    elif args.test or args.pdf:
        test_single_pdf(args.pdf, bib_path=args.bib)
    elif args.batch:
        batch_process_pdfs(
            max_papers=args.max,
            max_workers=args.workers,
            skip_existing=not args.force,
            bib_path=args.bib,
            per_key_concurrency=args.per_key,
            max_retries=args.retries,
        )
    else:
        print("默认模式: 测试单个PDF")
        print("使用 --batch 进行批量处理")
        print("使用 --merge 按subsubsection聚合")
        print("使用 --pdf <path> 指定PDF文件")
        print()
        test_single_pdf(bib_path=args.bib)
