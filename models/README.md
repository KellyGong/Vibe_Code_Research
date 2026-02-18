# 常用与最新大模型汇总

本文档汇总当前常用/新发布的大模型信息，包括：**定价与订阅**、**模型规格**、**Benchmark 性能**、**用户评价**。数据截至 2026 年 2 月，来源于官方文档与社区公开信息。

---

## 一、模型定价对比

### 1.1 API 单次调用价格（每百万 tokens，美元）

| 模型 | Input ($/1M) | Output ($/1M) | 备注 |
|------|-------------|---------------|------|
| **Claude Opus 4.6** | 5.00 | 25.00 | 标准 ≤200K；>200K 为 10.00 / 37.50 |
| **Claude Sonnet 4.6** | 3.00 | 15.00 | >200K 为 6.00 / 22.50 |
| **Claude Opus 4.5** | 5.00 | 25.00 | 同 Opus 4.6 标准档 |
| **Claude Sonnet 4.5** | 3.00 | 15.00 | 同 Sonnet 4.6 |
| **GPT-5.3 Codex** | 1.75 | 14.00 | Cached input 0.175；reasoning 按 output 计费 |
| **GPT-5.3 Codex Spark** | — | — | Research Preview，暂无独立 API 价 |
| **Gemini 3 Pro** | 2.00 | 12.00 | ≤200K；>200K 为 4.00 / 18.00 |
| **Gemini 3 Flash** | 0.50 | 3.00 | 性价比极高 |
| **GLM-5** | 1.00 | 3.20 | MIT 开源，可自部署 |
| **Kimi K2.5** | 0.60 | 3.00 | Cache hit 0.10；约为 Claude 的 1/40 |
| **MiniMax M2.5** | 0.30 | 1.10 | Cache read 0.15；约为 Opus 4.6 的 1/10~1/20 |

### 1.2 订阅计划与请求额度概览

| 厂商/产品 | 计划 | 月费 | 主要额度/权益 |
|-----------|------|------|----------------|
| **Claude (Anthropic)** | Free | $0 | 仅 Sonnet 级，用量受限 |
| | Pro | $20 | 约 45 条/5h 滚动；有限 Opus |
| | Max 5x | $100 | 5× Pro 用量，完整 Opus |
| | Max 20x | $200 | 20× Pro，零延迟优先级 |
| | Team | $25–125/席 | 5–150 人，SSO、管理台 |
| **ChatGPT / Codex (OpenAI)** | Free | $0 | 有限 GPT-5.2 |
| | Plus | $20 | Codex agent、高级推理 |
| | Pro | $200 | 无限 GPT-5.2、Spark 预览、扩展 Codex |
| | Business | $25–30/用户 | 无限消息、SAML、合规 |
| **Google AI** | Free | $0 | 50 credits/日，Gemini 3 Flash 有限 |
| | AI Plus | $7.99 | 200 credits/月，Gemini 3 Pro |
| | AI Pro | $19.99 | 1000 credits/月，学生可免费用一年 |
| **智谱 (Z.ai) GLM-5** | API 按量 | — | $1/$3.2 per 1M；chat.z.ai 免费聊天 |
| **Kimi (月之暗面)** | Free | $0 | 约 150 万 tokens/日（视地区） |
| | Premium | $19.99 | 1,000 次对话/月 |
| | Starter | $5.99 | 250 次对话/月 |
| | Pro | $12.99 | 600 次对话/月 |
| **MiniMax** | Pay as You Go | — | 按 token；Coding Plan 支持 M2.5/M2.1/M2 |

> 具体条数/credits 以各平台当前文档为准；Pro/Max 等常采用 5 小时滚动或每周重置。

---

## 二、模型规格对比

| 模型 | Context Window | Max Output | Thinking/推理 | 多模态输入 | 备注 |
|------|----------------|------------|---------------|------------|------|
| **Claude Opus 4.6** | 200K（1M beta） | 128K | Adaptive（low/medium/high/max） | 文本+图像 | 1M 仅 API beta |
| **Claude Sonnet 4.6** | 200K（1M beta） | 64K | Adaptive + Extended | 文本+图像 | Computer Use 提升明显 |
| **Claude Opus 4.5** | 200K（1M beta） | 64K | Extended，effort 可调 | 文本+图像 | SWE-bench 曾最高 |
| **Claude Sonnet 4.5** | 200K（1M beta） | 64K | Extended thinking | 文本+图像 | 编程/Agent 强 |
| **GPT-5.3 Codex** | 400K | 128K | Reasoning effort: low/medium/high | 文本+图像 | Agentic 8h+ 长任务 |
| **GPT-5.3 Codex Spark** | 128K | — | 轻量推理 | 文本 | 1000+ tok/s，Cerebras |
| **Gemini 3 Pro** | 1M | 64K | Dynamic Thinking (LOW/HIGH) | 文本+图像+音视频+PDF | Deep Think 始终开启 |
| **Gemini 3 Flash** | 1M | 64K | Dynamic Thinking (minimal~high) | 文本+图像+视频+音频+PDF | ~218 tok/s |
| **GLM-5** | 200K | 128K | Reasoning mode 可选 | 文本 | 744B MoE，MIT 开源 |
| **Kimi K2.5** | 256K | 8K | Thinking / Instant 双模式 | 文本+图像+视频+PDF | 1T MoE，Agent Swarm |
| **MiniMax M2.5** | 204.8K | 长输出(含 CoT) | 推理优化 | 文本 | 230B MoE，Lightning 版 ~100 tok/s |

---

## 三、Benchmark 性能对比

### 3.1 编程与软件工程

| Benchmark | Opus 4.6 | Sonnet 4.6 | Opus 4.5 | GPT-5.3 Codex | Gemini 3 Pro | Gemini 3 Flash | GLM-5 | Kimi 2.5 | MiniMax M2.5 |
|-----------|----------|------------|----------|---------------|---------------|----------------|-------|----------|---------------|
| **SWE-bench Verified** | 80.8% | 79.6% | **80.9%** | — | 76.2% | 78.0% | 77.8% | 76.8% | **80.2%** |
| **Terminal-Bench 2.0** | 65.4% | — | 59.8% | **77.3%** | 56.2% | — | 56.2% | 50.8% | — |
| **OSWorld** | — | 72.5% | 66.3% | 64.7% | — | — | — | — | — |
| **LiveCodeBench** | — | — | — | — | — | 90.8% | — | **85.0%** | — |

### 3.2 推理与知识

| Benchmark | Opus 4.6 | Sonnet 4.6 | GPT-5.3 Codex | Gemini 3 Pro | Gemini 3 Flash | GLM-5 | Kimi 2.5 |
|-----------|----------|------------|---------------|---------------|----------------|-------|----------|
| **GPQA Diamond** | ~77% | 89.9% | 73.8% | **91.9%** | 90.4% | 68–86% | 87.6% |
| **MMLU / MMLU-Pro** | 85.1% | 89.3% | — | 92% | — | — | 87.1% |
| **ARC-AGI-2** | **68.8%** | 58.3% | — | 31–45% | 33.6% | — | — |
| **Humanity's Last Exam** | 40–53% | 33–49% | — | 38–46% | 33.7% | **50.4%** | **50.2%** |
| **AIME 2025** | ~94% | — | — | 95–100% | 99.7% | 88.7% | 96.1% |

### 3.3 小结

- **SWE-bench**：Opus 4.5/4.6、MiniMax M2.5 在 80% 左右领先；Codex 在 **Terminal-Bench 2.0** 领先（77.3%）。
- **长上下文**：Opus 4.6 在 MRCR v2（1M）约 76%；Gemini 3 系列为 1M context。
- **推理**：Opus 4.6 在 ARC-AGI-2 提升显著；Gemini 3 Pro 在 GPQA/MMLU 领先；GLM-5 在 HLE 表现突出。

---

## 四、各模型简介与用户评价

### 1. Claude Opus 4.6（Anthropic）

- **定位**：旗舰推理与长上下文，Adaptive Thinking，1M context（beta）。
- **亮点**：ARC-AGI-2 大幅提升、1M 上下文、128K 输出、Context Compaction、Agent Teams（research）。
- **用户评价**：长上下文与代码库理解获好评；部分反馈写作变“平淡”、过度自信需权限门控；Pro 用户 2–3 小时易触达限额；曾出现 API 配置回退导致多步任务性能下降，社区要求更高透明度。

### 2. Claude Sonnet 4.6（Anthropic）

- **定位**：性价比主力，Free/Pro 默认模型，兼顾编码与 Computer Use。
- **亮点**：1M context beta、OSWorld 72.5%、office/金融等场景超越部分 Opus 表现，价格 $3/$15。
- **用户评价**：“Sonnet 价格、Opus 4.5 级体验”；编码省 token；高复杂度仍倾向用 Opus；部分反馈 4.6 系列 token 消耗偏多。

### 3. Claude Opus 4.5（Anthropic）

- **定位**：上一代旗舰，SWE-bench Verified 曾达 80.9%，编程与 Agent 能力强。
- **亮点**：Extended thinking、effort 可调、token 效率高、Memory、Context Editing。
- **用户评价**：编程“像高级工程师”；存在过度自主、忽略指令、过度文档化等问题；适合编程密集型，通用任务可考虑 Sonnet 或竞品。

### 4. Claude Sonnet 4.5（Anthropic）

- **定位**：发布时“最佳编程模型”之一，Agent 与 Computer Use 强。
- **亮点**：SWE-bench Verified 77.2%+、OSWorld 61.4%、AIME 100%（带工具）、持久长任务。
- **用户评价**：专业团队反馈质量高；社区反映幻觉、忽略指令、长上下文检索弱（256K 时 MRCR 约 18.5%）；工具链（如 Claude Code vs Codex CLI）对效果影响大。

### 5. GPT-5.3 Codex（OpenAI）

- **定位**：Agentic 编程专用，长任务执行（8h+）、mid-task steering。
- **亮点**：400K context、128K 输出、三档 reasoning effort、Terminal-Bench 2.0 77.3%、网络安全 High capability、Spark 版 1000+ tok/s。
- **用户评价**：可“启动任务、几小时后回来看到可运行软件”；与 Opus 搭配（Opus 规划、Codex 执行）受推荐；Spark 适合快速迭代/审计，复杂推理仍用旗舰版；有静默路由到 5.2 的反馈；Spark 在精确编辑和 context 范围上存在局限。

### 6. Gemini 3 Pro（Google DeepMind）

- **定位**：1M context、Deep Think、多模态与 Agentic 编码。
- **亮点**：GPQA 91.9%、AIME 95–100%、MMLU 92%、多模态、Generative UI。
- **用户评价**：初期“明显优于 GPT-5.2 和 Opus 4.5”；后续反馈长上下文退化严重（50K+ 质量下降、600K–900K 理解差）、rate limit 缩减引发不满、幻觉与 API 不稳定；编码脚手架和重构获认可，但需人工审逻辑错误。

### 7. Gemini 3 Flash（Google DeepMind）

- **定位**：高性价比、低延迟、接近 Pro 的推理，$0.50/$3 per 1M。
- **亮点**：1M context、~218 tok/s、SWE-bench 78% 超 Gemini 3 Pro、Dynamic Thinking。
- **用户评价**：“Budget Model That Became My Default”；速度与性价比获好评；幻觉率仍高，关键输出需验证；免费额度大幅削减为主要抱怨点。

### 8. GLM-5（智谱 AI）

- **定位**：744B MoE、MIT 开源、国产全昇腾训练、低幻觉。
- **亮点**：200K context、128K 输出、Humanity's Last Exam 50.4%、BrowseComp 领先、幻觉率约 34%（行业较低）、API $1/$3.2。
- **用户评价**：工程能力接近 Opus 级；推理速度 17–19 tok/s 偏慢；Agent 编程与顶级闭源仍有差距；适合高性价比与事实准确性场景，复杂 Agent 可搭配闭源。

### 9. Kimi K2.5（月之暗面）

- **定位**：1T MoE、多模态、视觉编程、Agent Swarm（最多 100 agent）。
- **亮点**：256K context、截图/录屏转代码、OCR/文档理解领先、价格约为 Claude 的 1/40。
- **用户评价**：视觉编程与设计稿还原获好评；编程逻辑稳定性、temperature=0 下一致性（0%）受诟病；速度偏慢；适合前端/UI/文档场景与预算敏感项目。

### 10. MiniMax M2.5（稀宇科技）

- **定位**：编码/Agent/办公 SOTA，SWE-bench Verified 80.2%，高性价比。
- **亮点**：230B MoE、约 200K context、M2.5-Lightning ~100 tok/s、output $1.10/1M、BrowseComp 76.3%、开源。
- **用户评价**：性价比极高、“intelligence too cheap to meter”；复杂编码一致性与幻觉控制仍为短板；适合 Agent、写作、工具调用；高精度场景建议配合验证或更强模型。

---

## 五、如何选用（简要）

| 需求 | 可优先考虑 |
|------|------------|
| 长上下文 + 强推理 | Claude Opus 4.6（1M beta）、Gemini 3 Pro |
| 编程 + Agent 执行 | GPT-5.3 Codex、Claude Opus 4.6、MiniMax M2.5 |
| 性价比 + 编码 | Gemini 3 Flash、Sonnet 4.6、GLM-5、MiniMax M2.5 |
| 极速迭代 / 前端 | GPT-5.3 Codex Spark、Kimi K2.5（视觉编程） |
| 开源 / 自部署 | GLM-5、Kimi K2.5、MiniMax M2.5 |
| 文档 / OCR / 多模态 | Kimi K2.5、Gemini 3 系列 |

---

## 六、数据说明与更新

- **定价与额度**：以各厂商当前官网/文档为准，可能有地域与活动差异。
- **Benchmark**：不同评测批次、设置（pass@k、有无工具、thinking 档位）会导致差异，表中为近似对比。
- **用户评价**：来自 Reddit、Hacker News、知乎、V2EX、掘金等公开讨论，为主观体验汇总。

详细单模型报告见：`models/tmp/` 下对应 `opus46.md`、`sonnet46.md`、`opus45.md`、`sonnet45.md`、`gpt53codex.md`、`gemini3pro.md`、`gemini3flash.md`、`glm5.md`、`kimi25.md`、`minimax25.md`。

*文档最后更新：2026 年 2 月*
