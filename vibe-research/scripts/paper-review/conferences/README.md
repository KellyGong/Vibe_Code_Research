# 会议要求查询指南

## 概述

不同学术会议有不同的投稿要求。本模块不预置会议要求，而是在审稿时实时查询最新的官方要求。

## 查询流程

### 第一步：构建搜索查询

```
搜索模板：
"[会议名称] [年份] author guidelines"
"[会议名称] [年份] call for papers"
"[会议名称] [年份] submission requirements"
```

### 第二步：定位官方页面

优先访问以下来源：
- 会议官方网站
- ACL Anthology（NLP会议）
- OpenReview（ML会议）

### 第三步：提取关键要求

需要提取的信息：

| 类别 | 具体项目 |
|------|---------|
| **格式要求** | 页数限制、模板、字体、边距 |
| **匿名化** | 是否双盲、匿名化要求 |
| **引用格式** | numbered vs author-year |
| **必需章节** | Ethics Statement, Limitation, Broader Impact |
| **Checklist** | Reproducibility Checklist, Ethics Checklist |
| **附录** | 是否允许、页数限制 |
| **代码/数据** | 是否要求提交、匿名化要求 |

## 常见会议快速参考

以下信息仅供参考，**务必查询最新官方要求**：

### NLP 会议 (ACL/EMNLP/NAACL/EACL/COLING)

```
通常要求：
- 长文 8 页，短文 4 页（不含参考文献）
- 附录无限制
- 双盲审稿
- 使用 ACL 模板
- 需要 Limitation section
- 需要 Ethics Statement（如适用）
- 可能需要 Reproducibility Checklist
```

### ML 会议 (NeurIPS/ICML/ICLR)

```
通常要求：
- 正文 9 页（不含参考文献和附录）
- 双盲审稿
- 使用会议官方模板
- 可能需要 Broader Impact Statement
- NeurIPS 需要 Reproducibility Checklist
```

### CV 会议 (CVPR/ICCV/ECCV)

```
通常要求：
- 正文 8 页（不含参考文献）
- 双盲审稿
- 使用会议官方模板
```

### AI 会议 (AAAI/IJCAI)

```
通常要求：
- AAAI: 7 页 + 参考文献
- IJCAI: 7 页 + 参考文献
- 双盲审稿
```

## 输出格式

查询会议要求后，输出以下格式：

```markdown
## [会议名称] [年份] 投稿要求

**来源**: [官方链接]
**查询日期**: [日期]

### 格式要求
- 正文页数: X 页
- 模板: [链接]
- 参考文献: [是否计入页数]
- 附录: [要求]

### 审稿模式
- [双盲/单盲/开放]
- 匿名化要求: [具体要求]

### 必需章节
- [ ] Limitation Section: [要求/否]
- [ ] Ethics Statement: [要求/否]
- [ ] Broader Impact: [要求/否]
- [ ] Reproducibility Checklist: [要求/否]

### 其他要求
[其他特殊要求]
```

## 注意事项

1. **时效性**：会议要求每年可能变化，务必查询最新版本
2. **Track差异**：同一会议不同Track（main/findings/demo）要求可能不同
3. **截止日期**：注意区分投稿截止和camera-ready要求
4. **模板版本**：使用最新版本模板，旧版可能导致格式问题
