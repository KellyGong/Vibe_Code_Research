#!/usr/bin/env python3
"""
思维导图可视化和管理工具
提供Web界面来查看、管理和编辑论文分类
"""

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, jsonify, render_template, request, send_from_directory

# 配置路径
SCRIPT_DIR = Path(__file__).parent.absolute()
MINDMAP_ROOT = SCRIPT_DIR / "mindmap_v2"
BY_SUBSECTION_DIR = MINDMAP_ROOT / "by_subsubsection"
PAPER_JSON_DIR = MINDMAP_ROOT / "paper_json"
PAPER_MINDMAP_DIR = MINDMAP_ROOT / "paper_mindmaps"

app = Flask(__name__)


def parse_mindmap_markdown(md_path: Path) -> List[Dict[str, Any]]:
    """解析mindmap markdown文件，提取论文条目"""
    if not md_path.exists():
        return []

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    items = []
    lines = content.split("\n")
    current_item: Optional[Dict[str, Any]] = None
    current_section: Optional[str] = None

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # 检测论文标题行（以 "- " 开头，但不是缩进的）
        if line.startswith("- ") and not line.startswith("    - "):
            # 保存上一个item
            if current_item is not None:
                items.append(current_item)

            # 开始新item
            title = line[2:].strip()
            current_item = {
                "title": title,
                "bib_key": "",
                "summary": "",
                "details": [],
                "contributions": [],
                "training_data": "",
                "objective_or_loss": "",
                "signals_or_tools": "",
                "datasets": [],
                "metrics_or_results": [],
                "scientific_findings": [],
            }
            current_section = None

        elif current_item is not None:
            # BibTeXKey
            if line.strip().startswith("- BibTeXKey:"):
                current_item["bib_key"] = line.split(":", 1)[1].strip()

            # Summary
            elif line.strip().startswith("- Summary:"):
                current_item["summary"] = line.split(":", 1)[1].strip()

            # Details
            elif line.strip() == "- Details:":
                current_section = "details"
                current_item["details"] = []

            # Contribution
            elif line.strip().startswith("- Contribution:"):
                current_section = "contributions"
                current_item["contributions"] = []

            # Training data
            elif line.strip().startswith("- Training data:"):
                current_item["training_data"] = line.split(":", 1)[1].strip()

            # Objective/Loss
            elif line.strip().startswith("- Objective/Loss:"):
                current_item["objective_or_loss"] = line.split(":", 1)[1].strip()

            # Signals/Tools
            elif line.strip().startswith("- Signals/Tools:"):
                current_item["signals_or_tools"] = line.split(":", 1)[1].strip()

            # Datasets
            elif line.strip() == "- Datasets:":
                current_section = "datasets"
                current_item["datasets"] = []

            # Metrics/Results
            elif line.strip() == "- Metrics/Results:":
                current_section = "metrics_or_results"
                current_item["metrics_or_results"] = []

            # Scientific findings
            elif line.strip() == "- Scientific findings:":
                current_section = "scientific_findings"
                current_item["scientific_findings"] = []

            # 列表项（Details, Contributions等）
            elif current_section and line.strip().startswith("- "):
                item_text = line.strip()[2:].strip()
                # 处理编号列表（如 "1. xxx"）
                if re.match(r"^\d+\.\s", item_text):
                    item_text = re.sub(r"^\d+\.\s", "", item_text)
                current_item[current_section].append(item_text)

            elif current_section and line.strip().startswith("    - "):
                item_text = line.strip()[6:].strip()
                if re.match(r"^\d+\.\s", item_text):
                    item_text = re.sub(r"^\d+\.\s", "", item_text)
                current_item[current_section].append(item_text)

        i += 1

    # 保存最后一个item
    if current_item is not None:
        items.append(current_item)

    return items


def get_category_structure() -> Dict[str, Any]:
    """获取分类树形结构"""
    structure = {}

    for section_dir in BY_SUBSECTION_DIR.iterdir():
        if not section_dir.is_dir():
            continue

        section_name = section_dir.name
        structure[section_name] = {}

        # Application目录下的文件直接是任务
        if section_name == "Application":
            for task_file in section_dir.glob("*.md"):
                task_name = task_file.stem
                structure[section_name][task_name] = {
                    "path": str(task_file.relative_to(MINDMAP_ROOT)),
                    "full_path": str(task_file),
                    "subsection": task_name,
                    "subsubsection": task_name,
                }
        else:
            # Representation和Cognition有subsection和subsubsection
            for subsection_dir in section_dir.iterdir():
                if not subsection_dir.is_dir():
                    continue

                subsection_name = subsection_dir.name
                structure[section_name][subsection_name] = {}

                for subsub_file in subsection_dir.glob("*.md"):
                    subsub_name = subsub_file.stem
                    structure[section_name][subsection_name][subsub_name] = {
                        "path": str(subsub_file.relative_to(MINDMAP_ROOT)),
                        "full_path": str(subsub_file),
                        "subsection": subsection_name,
                        "subsubsection": subsub_name,
                    }

    return structure


def get_all_categories_flat() -> List[Dict[str, str]]:
    """获取所有分类的扁平列表，用于下拉菜单"""
    categories = []
    structure = get_category_structure()

    for section_name, section_data in structure.items():
        if section_name == "Application":
            for task_name, task_info in section_data.items():
                categories.append({
                    "section": section_name,
                    "subsection": task_name,
                    "subsubsection": task_name,
                    "display_name": f"{section_name} / {task_name}",
                    "path": task_info["path"],
                })
        else:
            for subsection_name, subsection_data in section_data.items():
                for subsub_name, subsub_info in subsection_data.items():
                    categories.append({
                        "section": section_name,
                        "subsection": subsection_name,
                        "subsubsection": subsub_name,
                        "display_name": f"{section_name} / {subsection_name} / {subsub_name}",
                        "path": subsub_info["path"],
                    })

    return sorted(categories, key=lambda x: x["display_name"])


@app.route("/")
def index():
    """主页"""
    return render_template("index.html")


@app.route("/api/structure")
def api_structure():
    """获取分类结构"""
    return jsonify(get_category_structure())


@app.route("/api/categories")
def api_categories():
    """获取所有分类（扁平列表）"""
    return jsonify(get_all_categories_flat())


@app.route("/api/category/<path:category_path>")
def api_category_items(category_path: str):
    """获取某个分类下的论文列表"""
    md_path = MINDMAP_ROOT / category_path
    if not md_path.exists():
        return jsonify({"error": "Category not found"}), 404

    items = parse_mindmap_markdown(md_path)
    return jsonify({
        "path": category_path,
        "items": items,
    })


@app.route("/api/paper/<paper_id>")
def api_paper_json(paper_id: str):
    """获取论文的JSON数据"""
    json_path = PAPER_JSON_DIR / f"{paper_id}.json"
    if not json_path.exists():
        return jsonify({"error": "Paper not found"}), 404

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def extract_item_from_markdown(content: str, item_title: str, item_bib_key: str) -> Tuple[Optional[str], str]:
    """从markdown内容中提取指定的item，返回(item_md, remaining_content)"""
    lines = content.split("\n")
    item_start = -1
    item_end = -1
    
    # 找到item的起始位置
    for i, line in enumerate(lines):
        # 检测item开始行（以 "- " 开头，不是缩进的）
        if line.startswith("- ") and not line.startswith("    - "):
            if item_title in line:
                # 检查bib_key是否匹配（如果提供了）
                if item_bib_key:
                    # 查看后续行是否有匹配的BibTeXKey
                    found_bib_key = False
                    for j in range(i + 1, min(i + 20, len(lines))):
                        if lines[j].strip().startswith("- BibTeXKey:"):
                            if item_bib_key in lines[j]:
                                found_bib_key = True
                            break
                        # 如果遇到下一个顶级item，停止查找
                        if lines[j].startswith("- ") and not lines[j].startswith("    - "):
                            break
                    
                    if not found_bib_key:
                        # BibKey不匹配，跳过这个item
                        continue
                
                item_start = i
                break
    
    if item_start == -1:
        return None, content
    
    # 找到item的结束位置（下一个顶级item或文件结束）
    item_end = len(lines)
    for i in range(item_start + 1, len(lines)):
        line = lines[i]
        # 如果遇到下一个顶级item（以 "- " 开头，不是缩进的），停止
        if line.startswith("- ") and not line.startswith("    - "):
            item_end = i
            break
    
    # 提取item和剩余内容
    item_lines = lines[item_start:item_end]
    remaining_lines = lines[:item_start] + lines[item_end:]
    
    item_md = "\n".join(item_lines).rstrip()
    remaining_md = "\n".join(remaining_lines)
    
    return item_md, remaining_md


@app.route("/api/move", methods=["POST"])
def api_move_item():
    """移动item到另一个分类"""
    data = request.json
    source_path = data.get("source_path")
    target_path = data.get("target_path")
    item_title = data.get("item_title")
    item_bib_key = data.get("item_bib_key") or ""

    if not all([source_path, target_path, item_title]):
        return jsonify({"error": "Missing parameters"}), 400

    source_md = MINDMAP_ROOT / source_path
    target_md = MINDMAP_ROOT / target_path

    if not source_md.exists() or not target_md.exists():
        return jsonify({"error": "Category not found"}), 404

    # 读取源文件和目标文件
    with open(source_md, "r", encoding="utf-8") as f:
        source_content = f.read()

    with open(target_md, "r", encoding="utf-8") as f:
        target_content = f.read()

    # 从源文件中提取要移动的item
    item_md, remaining_content = extract_item_from_markdown(source_content, item_title, item_bib_key)
    
    if not item_md:
        return jsonify({"error": "Item not found in source"}), 404

    # 检查目标文件中是否已存在
    target_items = parse_mindmap_markdown(target_md)
    for item in target_items:
        if item["title"] == item_title and item.get("bib_key") == item_bib_key:
            return jsonify({"error": "Item already exists in target"}), 400

    # 将item添加到目标文件（在</mindmap>之前）
    target_lines = target_content.split("\n")
    new_target_lines = []
    for line in target_lines:
        if line.strip() == "</mindmap>":
            # 在</mindmap>之前添加item，确保有换行
            if new_target_lines and new_target_lines[-1].strip():
                new_target_lines.append("")
            new_target_lines.append(item_md)
            new_target_lines.append("")
            new_target_lines.append(line)
        else:
            new_target_lines.append(line)

    # 写回文件
    try:
        with open(source_md, "w", encoding="utf-8") as f:
            f.write(remaining_content)

        with open(target_md, "w", encoding="utf-8") as f:
            f.write("\n".join(new_target_lines))
    except Exception as e:
        return jsonify({"error": f"File write error: {str(e)}"}), 500

    return jsonify({"success": True})


@app.route("/api/delete", methods=["POST"])
def api_delete_item():
    """删除item"""
    data = request.json
    source_path = data.get("source_path")
    item_title = data.get("item_title")
    item_bib_key = data.get("item_bib_key") or ""

    if not all([source_path, item_title]):
        return jsonify({"error": "Missing parameters"}), 400

    source_md = MINDMAP_ROOT / source_path
    if not source_md.exists():
        return jsonify({"error": "Category not found"}), 404

    # 读取源文件
    with open(source_md, "r", encoding="utf-8") as f:
        source_content = f.read()

    # 从源文件中删除item
    _, remaining_content = extract_item_from_markdown(source_content, item_title, item_bib_key)

    # 写回文件
    try:
        with open(source_md, "w", encoding="utf-8") as f:
            f.write(remaining_content)
    except Exception as e:
        return jsonify({"error": f"File write error: {str(e)}"}), 500

    return jsonify({"success": True})


def format_item_markdown(item: Dict[str, Any]) -> str:
    """将item字典格式化为markdown格式"""
    lines = [f"- {item['title']}"]
    
    if item.get("bib_key"):
        lines.append(f"    - BibTeXKey: {item['bib_key']}")
    
    if item.get("summary"):
        lines.append(f"    - Summary: {item['summary']}")
    
    if item.get("details"):
        lines.append("    - Details:")
        for detail in item["details"]:
            lines.append(f"        - {detail}")
    
    if item.get("contributions"):
        lines.append("    - Contribution:")
        for i, contrib in enumerate(item["contributions"], 1):
            lines.append(f"        {i}. {contrib}")
    
    if item.get("training_data"):
        lines.append(f"    - Training data: {item['training_data']}")
    
    if item.get("objective_or_loss"):
        lines.append(f"    - Objective/Loss: {item['objective_or_loss']}")
    
    if item.get("signals_or_tools"):
        lines.append(f"    - Signals/Tools: {item['signals_or_tools']}")
    
    if item.get("datasets"):
        lines.append("    - Datasets:")
        for dataset in item["datasets"]:
            lines.append(f"        - {dataset}")
    
    if item.get("metrics_or_results"):
        lines.append("    - Metrics/Results:")
        for metric in item["metrics_or_results"]:
            lines.append(f"        - {metric}")
    
    if item.get("scientific_findings"):
        lines.append("    - Scientific findings:")
        for finding in item["scientific_findings"]:
            lines.append(f"        - {finding}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 创建templates目录
    templates_dir = SCRIPT_DIR / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # 创建static目录
    static_dir = SCRIPT_DIR / "static"
    static_dir.mkdir(exist_ok=True)
    
    app.run(host="0.0.0.0", port=5000, debug=True)

