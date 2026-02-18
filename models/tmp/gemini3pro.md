# Gemini 3 Pro — Google DeepMind

> 调研时间：2026年2月  
> 模型发布日期：2025年11月18日  
> 模型 ID：`gemini-3-pro-preview`  
> 知识截止日期：2025年1月  
> 架构：Mixture of Experts (MoE) Transformer + Deep Think 推理层

---

## 1. 定价 (Pricing)

### 1.1 API 定价 — Google AI Studio / Gemini Developer API

| 项目 | ≤200K context | >200K context |
|------|--------------|---------------|
| Input (每 1M tokens) | $2.00 | $4.00 |
| Output (每 1M tokens) | $12.00 | $18.00 |

**Batch 批量处理（50% 折扣）：**

| 项目 | ≤200K context | >200K context |
|------|--------------|---------------|
| Input (每 1M tokens) | $1.00 | $2.00 |
| Output (每 1M tokens) | $6.00 | $9.00 |

**Context Caching：**
- 缓存 token 费用：$0.20–$0.40 / 1M tokens（取决于 context 大小）
- 缓存存储费用：$4.50 / 1M tokens / 小时
- 最低缓存命中要求：4,096 input tokens
- 默认 TTL：60 分钟

**Grounding with Google Search：**
- $14 / 1,000 次搜索查询
- 每月前 5,000 次 prompt 免费

### 1.2 Vertex AI 定价（企业级）

| Tier | Input (每 1M tokens) | Output (每 1M tokens) |
|------|---------------------|----------------------|
| Standard | $2.00 | $12.00 |
| Priority | $3.60 | $21.60 |
| Flex/Batch | $1.00 | $6.00 |

- Image output 费用：$120 / 1M tokens（Standard tier）

### 1.3 消费者订阅计划 (Google One AI)

| 计划 | 月费 | AI Credits | 主要权益 |
|------|------|------------|---------|
| Free | 免费 | 50/天 | Gemini 3 Flash 有限访问 |
| Google AI Plus | $7.99/月（首2月 $3.99） | 200/月 | Gemini 3 Pro 增强访问 |
| Google AI Pro | $19.99/月（首月免费） | 1,000/月 | Gemini 3 Pro 高级访问 + 2TB 存储 |

- 大学生可免费获得 Google AI Pro 一年
- AI Plus 和 Pro 均包含：Deep Research、图像生成、Veo 3 视频生成、Gmail/Docs/Sheets 集成

### 1.4 API Rate Limits（速率限制）

**Free Tier（免费层）：**

| 指标 | 限制 |
|------|------|
| RPM (Requests Per Minute) | 5–10 |
| RPD (Requests Per Day) | 100 |
| TPM (Tokens Per Minute) | 250,000（所有免费模型共享） |

> ⚠️ 2025年12月7日，Google 大幅削减免费层配额：Pro 模型 RPM 降低 67%（15→5），RPD 降低 80%（500→100）。

**Tier 1（付费层 — 开通 billing 即可）：**

| 指标 | 限制 |
|------|------|
| RPM | 150–300 |
| TPM | 1–2M |
| RPD | 1,000–10,000 |

**Tier 2（累计消费 $250+ 且开通 30 天以上）：**

| 指标 | 限制 |
|------|------|
| RPM | 500–2,000 |
| TPM | 2M |
| RPD | 10,000+ |

**Tier 3 / Enterprise（累计消费 $1,000+ 或联系销售）：**
- RPM 可达 4,000+
- 自定义限制

> 注意：Rate limits 按 Google Cloud project 计算，非按 API key。RPD 配额每天太平洋时间午夜重置。免费 credits 不计入 Tier 升级消费门槛。

---

## 2. 模型规格 (Model Specs)

### 2.1 核心参数

| 参数 | 值 |
|------|-----|
| Context Window | 1,000,000 tokens (1M) |
| Maximum Output Tokens | 64,000 tokens |
| 架构 | Mixture of Experts (MoE) Transformer |
| 推理模式 | Dynamic Thinking（始终开启，不可关闭） |
| Thinking Level 参数 | `LOW` 或 `HIGH`（默认 `HIGH`） |
| 多模态输入 | 文本、图像、音频、视频、PDF、代码 |
| Media Resolution 参数 | `low` / `medium` / `high` |
| 模型 ID | `gemini-3-pro-preview` |
| 发布日期 | 2025年11月18日 |
| 知识截止 | 2025年1月 |

### 2.2 Thinking / Reasoning 能力

- **Dynamic Thinking**：Gemini 3 Pro 的推理模式始终激活，无法关闭
- 使用 `thinking_level` 参数控制推理深度（替代 Gemini 2.5 的 `thinking_budget`）
- `thinking_level: HIGH` — 深度推理，适合数学、编程、复杂分析任务
- `thinking_level: LOW` — 轻量推理，降低延迟和成本
- **Deep Think** 模式：多步骤推理，评估多条逻辑路径后再给出答案，显著减少幻觉
- 在 ARC-AGI-2 上，Deep Think 模式将得分从 31.1% 提升至 45.1%

### 2.3 关键特性

- **Agentic Coding**：支持自主导航文件系统、运行终端命令、自我调试的 agentic 循环
- **Vibe Coding**：从自然语言描述直接生成前端交互界面
- **Generative UI**：生成带有 widgets、地图等交互组件的富界面（而非纯文本列表）
- **Streaming Function Calling**：流式函数调用 + 多模态函数响应
- **Multi-tower Encoder**：多塔编码器系统，分别处理不同模态后统一推理
- **Context Caching**：支持隐式缓存（implicit caching），最低 4,096 tokens 触发

### 2.4 与 Gemini 2.5 Pro 的对比

| 维度 | Gemini 3 Pro | Gemini 2.5 Pro |
|------|-------------|----------------|
| Humanity's Last Exam | 37.5% | 21.6% |
| GPQA Diamond | 91.9% | 86.4% |
| AIME 2025 | 95.0% | 88.0% |
| 架构 | MoE + Deep Think + 增强规划循环 | 标准 MoE Transformer |
| Agentic 能力 | 多文件逻辑、自我调试、文件系统导航 | 多文件和自我调试能力较弱 |
| UI 生成 | 交互式富界面（widgets、地图） | 标准文本列表 |
| 推理控制 | `thinking_level` (LOW/HIGH) | `thinking_budget` (token 数) |
| Input 定价 | $2.00–$4.00 / 1M tokens | $1.50 / 1M tokens |
| 幻觉率 | 更低 | 较高 |
| 推理速度 | 更快 | 较慢 |
| 复杂工程任务 | 提升约 50% | 基线 |

---

## 3. Benchmark 成绩

### 3.1 推理与学术知识

| Benchmark | 得分 | 备注 |
|-----------|------|------|
| AIME 2025 | 95.0% | 无工具 |
| AIME 2025 (w/ code execution) | 100% | 使用代码执行 |
| GPQA Diamond | 91.9% | PhD 级别科学知识 |
| Humanity's Last Exam (HLE) | 37.5% | 无工具 |
| HLE (w/ search + code) | 45.8% | 使用搜索和代码执行 |
| MMLU | 92% | 57 个学科通用知识 |
| MMLU-Pro | 92% | 更难版本 |

### 3.2 编程能力

| Benchmark | 得分 | 备注 |
|-----------|------|------|
| SWE-bench Verified | 76% | 真实 GitHub issue 修复 |
| SWE-bench (标准) | 74.2% | 落后于 Claude Opus 4.6 (79.2%)，略低于 Claude Opus 4.5 (74.4%) |
| LiveCodeBench Pro | ELO 评分制 | 竞争性编程生成 |
| 独立编程测试 | 87.5% (35/40) | 中位完成时间 12.4 秒 |

### 3.3 多模态与视觉

| Benchmark | 得分 | 备注 |
|-----------|------|------|
| MMMU-Pro | 81.0% | Standard (10选项) + Vision 平均 |
| Video-MMMU | 87.6% | 视频时空推理 |
| ARC-AGI-2 | 31.1% | 抽象视觉推理（ARC Prize Verified） |
| ARC-AGI-2 (Deep Think) | 45.1% | Deep Think 模式 |

### 3.4 数学

| Benchmark | 得分 | 备注 |
|-----------|------|------|
| MathArena Apex | >20x 提升 | 相比前代模型 |
| AIME 2025 | 95%–100% | 见上方推理部分 |

> 评估方法说明：所有 Gemini 3 Pro 得分均使用 pass@1 方法，单次尝试，无 majority voting，通过 Gemini API 默认采样设置运行。小型 benchmark 结果为多次试验平均值。

---

## 4. 用户评价 (User Reviews)

### 4.1 Reddit 社区

**正面评价：**
- 发布初期被认为"freaking amazing"，在通用任务和代码方面"clearly superior to GPT-5.2 and Opus 4.5"
- 擅长生成结构良好、符合惯用法的代码
- 能够生成完整的前后端脚手架应用
- 重构能力强，能建议使用 `functools.lru_cache` 等优化

**负面评价：**
- 多位用户反映发布数周后质量明显下降："it's gone to shit the past two weeks"
- **Context 退化严重**：超过 50,000 tokens 后质量"plummeting"，600K–900K tokens 时难以正确理解上下文
- 尽管宣传 1M token context window，实际使用中需要每 500K tokens 重启对话
- 会引入微妙的逻辑错误，需要人工审查
- 对项目特定的 error schema 和 edge case 处理不佳

**Rate Limits 抱怨：**
- AI Studio 每日 token 限额从约 100 万降至约 5 万
- 重置机制从 24 小时窗口改为 3 小时滚动限制
- 部分用户不到 100 个 prompt 就触发限制
- 有用户因此取消订阅，称服务"unusable"

> r/GeminiAI 热帖标题："Gemini 3 Pro overrated?"

### 4.2 Hacker News 开发者

**编码体验：**
- "I don't see the benchmark gains of 3 Pro over 2.5 Pro reflected in my daily use at all. There's definitely none of that 'wow-factor' when Gemini 2.5 was released."
- 与竞品对比排名（某开发者观点）：
  - Cursor Composer：快速，适合一次性代码修改
  - Claude Code：有清晰计划时效果好，但质量全天波动
  - Codex CLI (GPT-5+high)：最慢但指令遵循最可靠
  - Gemini CLI：rate limits 较低，可用性挑战
- "I cannot get any of the Google models to stop outputting code comments constantly and everywhere"（无法让 Google 模型停止到处输出代码注释）
- API 经常无故不可用："the API frequently becomes unavailable for some reason"

**Agentic 使用：**
- Gemini CLI 配合 Gemini 3 Pro 可用于 agentic coding，但开发者反映 agentic 设置经常很快过时
- 有开发者认为 agentic 工具对复杂自定义任务"aren't reliable enough"

### 4.3 独立测试与评测

- 一项独立编程测试中，Gemini 3 Pro 在 40 道编程题中完成 35 道（87.5%），中位完成时间 12.4 秒，与 GPT-4o 和 Claude 3.5 Sonnet 相比表现良好
- 擅长 SVG 图形生成、HTML5 桌面界面、网页 mockup
- 在扫描文档、图表、UI 截图等复杂多模态输入上表现优于前代

### 4.4 幻觉问题 (Hallucination)

- Gemini 3 系列（包括 Flash）在小众话题上仍存在显著幻觉问题
- 模型会自信地编造关于不太知名的书籍或艺术家的信息，而非承认不确定
- 与 ChatGPT 不同，Gemini 缺乏强健的不确定性检测机制，不会在不确定时主动搜索网络
- Google 已添加"double check"功能帮助验证回答

### 4.5 综合评价总结

| 维度 | 评价 |
|------|------|
| 编码能力 | 强，尤其是脚手架生成和重构，但有微妙逻辑错误 |
| 推理深度 | Benchmark 优秀，但日常使用感知提升不明显 |
| 速度 | 较快，中位编程任务 12.4 秒 |
| 长上下文可靠性 | 差，50K tokens 后退化，与宣传的 1M 差距大 |
| API 稳定性 | 不稳定，频繁不可用 |
| Rate Limits | 免费层大幅缩减，付费层尚可但仍有抱怨 |
| 幻觉 | 小众话题仍严重，缺乏不确定性检测 |
| 性价比 | Input $2–4/1M tokens，比 2.5 Pro 贵，但能力更强 |

---

## 5. 访问方式

- **Google AI Studio**：免费层 + 付费 API
- **Vertex AI**：企业级部署
- **Gemini App**（移动端 + 网页端）：通过 Google One AI 订阅
- **Gemini CLI**：命令行工具，支持 agentic coding
- **Google Antigravity**：新的 agentic 开发平台
- **Google Workspace**：Gmail、Docs、Sheets、Slides、Meet 集成
- **Chrome / Android**：系统级集成

---

*数据来源：Google DeepMind 官方文档、Vertex AI 文档、Google AI Studio 定价页、Reddit (r/GeminiAI, r/Bard, r/GoogleGeminiAI, r/vibecoding)、Hacker News、独立评测网站。部分数据基于 Preview 版本，正式版可能有变化。*
