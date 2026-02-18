# Gemini 3 Flash — Google DeepMind

> 发布日期：2025 年 12 月 17 日
> 开发者：Google DeepMind
> 定位：高性价比前沿模型，兼顾速度与推理能力

---

## 1. 定价（Pricing）

### 1.1 Gemini API / Google AI Studio 定价（per 1M tokens）

| 类别 | 价格 |
|------|------|
| Text/Image/Video Input | $0.50 |
| Text Output | $3.00 |
| Audio Input | $1.00 |
| Context Caching（缓存读取） | $0.05 |

对比参考：

| 模型 | Input (per 1M) | Output (per 1M) |
|------|----------------|-----------------|
| Gemini 2.5 Flash | $0.30 | $2.50 |
| Gemini 3 Flash | $0.50 | $3.00 |
| Gemini 2.5 Pro | $1.25 | $10.00 |
| Gemini 3 Pro (≤200K) | $2.00 | $12.00 |
| Gemini 3 Pro (>200K) | $4.00 | $18.00 |
| Claude Opus 4.5 | $5.00 | — |
| GPT-5.2 | ~$1.75 | ~$13.80 |

Gemini 3 Flash 比 GPT-5.2 便宜约 3.5 倍（input）和 4.6 倍（output）。虽然单价略高于 Gemini 2.5 Flash，但由于平均 token 消耗减少约 30%，实际成本可能持平甚至更低。

### 1.2 Vertex AI 定价

与 Gemini API 一致：

- Input: $0.50 / 1M tokens
- Output: $3.00 / 1M tokens
- Cache Read: $0.05 / 1M tokens
- 支持 Batch Processing（批量处理），可降低约 50% 成本

### 1.3 Google AI Studio Free Tier（免费层）

免费层可用，无需信用卡：

| 限制维度 | 额度 |
|----------|------|
| RPM（每分钟请求数） | 5–15 |
| TPM（每分钟 token 数） | 250,000 |
| RPD（每日请求数） | 20（2025 年 12 月从 250 大幅削减至 20） |
| Google Search Grounding | 每月 5,000 次免费 |

注意：Gemini 3 Pro 无免费层，必须付费使用。

### 1.4 付费层级（Paid Tiers）Rate Limits

| 层级 | RPM | TPM | RPD | 要求 |
|------|-----|-----|-----|------|
| Free | 5–15 | 250K | 20 | 无需信用卡 |
| Tier 1 | 150–300 | 1–2M | 1,000–10,000 | 开通计费即可 |
| Tier 2 | 500–1,500 | 2M | 10,000+ | 累计消费 $250+，开通 30 天以上 |

- Rate limits 按 Google Cloud Project 计算，非按 API Key
- RPD 配额在太平洋时间午夜重置
- 超过任一维度限制即触发 429 错误

### 1.5 Google AI 订阅计划（消费者端）

| 计划 | 月费 | 主要权益 |
|------|------|----------|
| Google AI Plus | $7.99/月（促销 $3.99/月×2 个月） | Gemini 3 Pro 访问，200 AI credits，Veo 3 视频生成，200GB 存储 |
| Google AI Pro | $19.99/月（新用户首月免费，学生免费一年） | 更高 Gemini 3 Pro 额度，1,000 AI credits，Veo 3，200GB 存储 |
| Google AI Ultra | $250/月 | Gemini 2.5 Pro Deep Think 模式，Veo 3 早期访问，Imagen 4，30TB 存储，YouTube Premium |

---

## 2. 模型规格（Model Specs）

### 2.1 核心参数

| 参数 | 值 |
|------|-----|
| Context Window | 1,000,000 tokens（约 700,000 词 / 11 小时音频） |
| Maximum Output Tokens | 65,536 (64K) |
| 输出模态 | 仅文本（Text only） |
| 输出速度 | ~218 tokens/sec（GPT-5.2 约 125 tokens/sec） |
| 响应延迟 | ~20ms（比 Gemini 3 Pro 快 3 倍） |
| 发布日期 | 2025 年 12 月 17 日 |

### 2.2 Thinking / Reasoning 能力

Gemini 3 Flash 引入 Dynamic Thinking Mode（动态思考模式）：

- 使用 `thinking_level` 参数，支持四个级别：`minimal`、`low`、`medium`、`high`
- 替代了 Gemini 2.5 系列的 `thinking_budget` 参数
- 模型根据任务复杂度自动调整推理深度
- Thinking tokens 消耗 output token 配额，开启后成本增加但复杂任务准确率显著提升
- 简单查询无需开启；多步推理、代码调试、数学证明等场景效果显著

### 2.3 多模态能力（Multimodal Capabilities）

输入支持：
- Text（文本）
- Images（图像）— 支持 `media_resolution` 参数：low / medium / high / ultra high
- Video（视频）— 帧与音频分析
- Audio（音频）— 语音与声音模式识别
- PDF — 文档处理（文本、图表、表格）
- Code（代码）

特性：
- 统一架构，所有模态在单一推理管线中同时处理
- Cross-modal reasoning：可跨模态整合信息（如图文结合、视频+字幕分析）
- Function responses 可包含图像和 PDF 等多模态对象
- 支持复杂 agentic workflows

### 2.4 关键特性

- Native multimodality（原生多模态）
- Dynamic Thinking（动态推理）
- 1M token context window（业界最大之一，Claude Opus 4.5 为 200K）
- Function Calling — 可靠处理 100+ 工具同时调用
- Context Caching — 重复前缀可降低成本高达 90%
- Google Search Grounding — 实时搜索增强
- JSON Schema 输出
- 支持 System Messages

### 2.5 与 Gemini 2.5 Flash / Gemini 3 Pro 对比

| 维度 | Gemini 2.5 Flash | Gemini 3 Flash | Gemini 3 Pro |
|------|-------------------|----------------|--------------|
| Context Window | 1M | 1M | 1M |
| Max Output | 64K | 64K | 64K |
| Input 价格 | $0.30/1M | $0.50/1M | $2.00–$4.00/1M |
| Output 价格 | $2.50/1M | $3.00/1M | $12.00–$18.00/1M |
| SWE-bench Verified | ~60% | 78.0% | 76.2% |
| GPQA Diamond | ~70% | 90.4% | ~92% |
| MMMU-Pro | ~65% | 81.2% | ~83% |
| ARC-AGI-2 | ~5% | 33.6% | 31% |
| 速度 | 快 | 非常快（218 tok/s） | 较慢（~70 tok/s） |
| 适用场景 | 轻量任务 | 95% 生产场景 | 前沿推理、科研 |

核心结论：Gemini 3 Flash 在大多数 benchmark 上超越 Gemini 2.5 Pro，在编码任务上甚至超越 Gemini 3 Pro，同时成本仅为 Pro 的 1/4。

---

## 3. Benchmark 成绩

### 3.1 综合 Benchmark

| Benchmark | Gemini 3 Flash | 对比 |
|-----------|---------------|------|
| SWE-bench Verified（软件工程） | 78.0% | Claude Opus 4.5: ~80.9%, Gemini 3 Pro: 76.2% |
| GPQA Diamond（科学知识） | 90.4% | Claude Opus 4.5: ~89% |
| MMMU-Pro（多模态推理） | 81.2% | Claude Opus 4.5: ~79% |
| Humanity's Last Exam | 33.7% | Claude Opus 4.5: ~35% |
| ARC-AGI-2（视觉推理） | 33.6% | Gemini 3 Pro: 31%, Claude Sonnet 4.5: ~28%, GPT-5.2: 25% |
| AIME 2025（数学，with code execution） | 99.7% | — |
| SimpleQA（事实准确性） | 68.7%（准确率） | 从 Gemini 2.5 Flash 的 28.1% 大幅提升 |
| Artificial Analysis Intelligence Index | 71 | Claude 3 Opus: 70 |

### 3.2 编码 Benchmark

| Benchmark | Gemini 3 Flash | 备注 |
|-----------|---------------|------|
| SWE-bench Verified | 78.0% | 超越 Gemini 3 Pro (76.2%) |
| LiveCodeBench（Reasoning 模式） | 90.8% | 仅次于 Gemini 3 Pro Preview (high) 91.7% |
| LiveCodeBench Pro | ELO Rating 评估 | pass@1，默认 API 采样设置 |
| Terminal-Bench 2.0 | 领先 | — |
| Toolathlon | 领先 | — |
| MCP Atlas | 领先 | — |

### 3.3 Hallucination（幻觉）

- SimpleQA 事实准确率从 28.1%（2.5 Flash）提升至 68.7%，进步显著
- 但 hallucination rate 约 91%，比 2.5 Flash 高约 3 个百分点
- Vectara Hallucination Leaderboard（文档摘要任务）：Gemini 2.5 Flash 为 7.8%，Gemini 2.5 Flash Lite 为 3.3%
- 关键输出仍需人工验证

---

## 4. 用户评价（User Reviews）

### 4.1 Reddit 用户反馈

**正面评价：**
- 编码能力出色，SWE-bench 78% 超越 Gemini 3 Pro
- 有用户使用 Gemini Deep Think + Antigravity 审查 7K 行 Rust 代码库，一次性发现了隐藏数周的真实 bug
- 性价比极高，被称为"Budget Model That Became My Default"
- 在 AI Studio 中配合 grounding 使用效果显著优于网页版

**负面评价：**
- 幻觉问题严重：在冷门话题上会自信地编造信息，不像 ChatGPT 会主动搜索验证
- 不确定性检测（uncertainty detection）弱于 ChatGPT
- 网页版 Gemini 表现明显差于 AI Studio 版本
- 2025 年 12 月免费配额大幅削减（RPD 从 250 降至 20），引发开发者不满
- 部分用户认为在代码质量和可维护性方面仍不如 Claude Opus

来源：r/Bard, r/google_antigravity, r/vibecoding, r/opencodeCLI

### 4.2 Hacker News 开发者讨论

**高度正面的整体情绪：**

> "So fast and has such vast world knowledge that it's more performant than Claude Opus 4.5 or GPT 5.2 extra high, for a fraction of the inference time and price."

> "Much better results for 1/3rd of the price" — 某开发者对比 Gemini 2.5 Pro，响应快 5 秒，单用户成本从 20 美分降至 12 美分

- 在 Gemini CLI 中被认为"比 Claude Code 更快"，"生产力的质变"
- 开发者在内部产品 benchmark 中测试视频处理等多模态工作流，对输出准确率、处理时间、token 消耗和单请求成本均表示满意

来源：Hacker News item #46301851, #46351975

### 4.3 开发者博客与技术社区

**Better Stack 评测：**
- 速度极快，世界知识丰富
- Artificial Analysis Intelligence Index 得分 71，超过 Claude 3 Opus (70)
- SimpleQA 准确率大幅提升（28.1% → 68.7%）
- 但 hallucination rate 91% 仍然偏高，需要验证关键输出

**Thomas Wiegold 博客：**
- 称其为"My New Default"生产模型
- 比 GPT-5.2 快 1.7 倍（218 vs 125 tokens/sec）
- 适合 autocomplete、inline suggestions 等交互式编码工作流

**Vertu 技术分析：**
- Gemini 3 Flash 在编码 benchmark 上全面超越 Pro，说明架构优化比模型规模更重要
- 但 Gemini 3 Pro 存在严重的 memory issues（代码删除、上下文丢失）

### 4.4 总结：开发者共识

| 维度 | 评价 |
|------|------|
| 编码能力 | ⭐⭐⭐⭐ 优秀，SWE-bench 78%，超越多数竞品 |
| 速度 | ⭐⭐⭐⭐⭐ 极快，218 tok/s，延迟 ~20ms |
| 性价比 | ⭐⭐⭐⭐⭐ 业界最佳之一，$0.50/$3.00 per 1M |
| 推理能力 | ⭐⭐⭐⭐ 接近 Pro 水平，Dynamic Thinking 有效 |
| 多模态 | ⭐⭐⭐⭐ 原生支持，cross-modal reasoning 强 |
| 幻觉控制 | ⭐⭐⭐ 有改善但仍偏高，关键输出需验证 |
| 可靠性 | ⭐⭐⭐⭐ 整体稳定，但网页版不如 API 版 |
| 免费额度 | ⭐⭐ 2025 年 12 月大幅削减，开发者不满 |

---

## 5. 可用平台

- Google AI Studio（免费层 + 付费层）
- Vertex AI（Google Cloud）
- Gemini API
- Gemini CLI（付费用户 + API Key）
- Gemini App（已成为全球默认模型，替代 2.5 Flash）
- Google Search AI Mode
- Android Studio
- Antigravity

---

## 6. 关键结论

1. Gemini 3 Flash 打破了传统的"速度 vs 智能"权衡，以 Flash 级延迟提供接近 Pro 级推理
2. 在编码任务上（SWE-bench 78%）甚至超越了更昂贵的 Gemini 3 Pro（76.2%）
3. 1M token context window 是 Claude Opus 4.5（200K）的 5 倍
4. 成本仅为 Gemini 3 Pro 的 1/4，GPT-5.2 的 1/3.5
5. 幻觉问题仍是主要短板，SimpleQA 准确率虽从 28.1% 提升至 68.7%，但 hallucination rate 仍约 91%
6. 被多数开发者视为 95% 生产场景的最优默认选择，仅在前沿科研推理场景需要升级至 Pro
7. 免费层配额大幅削减是社区主要不满点

---

*数据收集日期：2026 年 2 月 19 日*
*信息来源：Google DeepMind 官方文档、Google Blog、Vertex AI 文档、Hacker News、Reddit、Better Stack、Artificial Analysis、开发者博客*
