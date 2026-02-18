# MiniMax（稀宇科技）模型全面调研

> 最后更新：2026年2月19日

## 1. 公司背景

- **全称**：MiniMax Group Inc.（稀宇科技）
- **成立时间**：2021年12月
- **总部**：上海
- **创始人**：闫俊杰（CEO）、杨斌、周宇聪，均来自商汤科技（SenseTime）计算机视觉团队
- **融资历史**：2024年3月，阿里巴巴领投6亿美元，估值25亿美元
- **港股IPO**：2026年1月9日在香港联交所上市，发行价 HK$165/股，首日收盘 HK$345（涨幅109.1%），募资约 HK$48亿（约6.19亿美元），上市首日市值约 HK$1,067亿（约137亿美元）
- **基石投资者**：阿里巴巴、阿布扎比主权基金、高瓴投资、红杉中国、IDG资本、腾讯等14家
- **核心产品**：Talkie（虚拟角色聊天，月活1100万）、海螺AI（Hailuo AI，多模态平台）、MiniMax Agent

---

## 2. 模型发布时间线

| 模型 | 发布时间 | 总参数量 | 激活参数量 | Context Window | 定位 |
|------|----------|----------|------------|----------------|------|
| MiniMax-Text-01 (MiniMax-01) | 2025年1月 | 456B | 45.9B | 1M tokens（推理可扩展至4M） | 基础语言模型 |
| MiniMax-M1 | 2025年6月 | 456B | 45.9B | 1M tokens | 推理模型（Reasoning） |
| MiniMax-M2 | 2025年10月 | 230B | 10B | 196,608 tokens | 编码与Agent模型 |
| MiniMax-M2.1 | 2025年12月 | 230B | 10B | 196,608 tokens | M2改进版 |
| MiniMax-M2 Her | 2026年1月 | — | — | 65,536 tokens | 角色扮演/对话 |
| **MiniMax-M2.5** | **2026年2月12日** | **230B** | **10B** | **204,800 tokens** | **编码/Agent/办公 SOTA** |

---

## 3. 模型架构详解

### 3.1 MiniMax-01 / M1 系列（456B）

基于 **Hybrid Attention + MoE** 架构：

- **总参数**：456B，每 token 激活 45.9B
- **层数**：80层
- **MoE 配置**：32个 expert，Top-2 routing 策略
- **Expert hidden dimension**：9,216
- **Attention heads**：64个，head dimension = 128
- **Hidden size**：6,144
- **Vocabulary size**：200,064
- **位置编码**：RoPE（base frequency = 10,000,000），应用于 attention head 维度的一半
- **核心创新 — Lightning Attention**：
  - 混合注意力设计：每7层 Lightning Attention 后接1层 Softmax Attention
  - 支持训练时 1M token context，推理时可外推至 4M tokens
  - 并行策略：LASP+（Linear Attention Sequence Parallelism Plus）、varlen ring attention、ETP（Expert Tensor Parallel）

### 3.2 M1 推理模型特有

- 全球首个开源大规模 hybrid-attention 推理模型
- 在 100K token 生成长度下，FLOPs 仅为 DeepSeek R1 的 **25%**
- 原生支持 1M token context（DeepSeek R1 的 **8倍**）
- RL 训练算法：**CISPO**（Clipped IS-weight Policy Optimization）
- 训练成本：512 × H800 GPU，3周完成，租赁费用约 $534,700

### 3.3 M2 / M2.5 系列（230B）

- **总参数**：230B，每 token 激活 **10B**（远小于 M1 的 45.9B）
- **架构**：稀疏 MoE
- **M2.5 Context Window**：204,800 tokens（约200K）
- **M2.5 最大输出 tokens**：支持长输出（含 Chain-of-Thought），M2 明确支持 128K output tokens
- **推理速度**：
  - M2.5 标准版：~50 tokens/sec
  - M2.5-Lightning（高速版）：~100 tokens/sec（其他前沿模型的约2倍）
- **开源**：已在 Hugging Face 开源，改进 MIT 许可证
- **部署支持**：SGLang、vLLM、Transformers，支持 FP8/BF16/F32

### 3.4 RL 训练框架 — Forge

- Agent-native RL 框架，完全解耦训练推理引擎与 Agent
- 支持任意 Agent 集成
- 异步调度策略优化系统吞吐
- 树结构合并训练样本，实现约 **40× 训练加速**
- 使用 CISPO 算法保证 MoE 模型大规模训练稳定性
- 引入 process reward 机制进行端到端生成质量监控

---

## 4. API 定价

### 4.1 文本模型定价（每 1M tokens，美元）

| 模型 | Input | Output | Cache Read | Context |
|------|-------|--------|------------|---------|
| MiniMax-01 | $0.20 | $1.10 | — | 1,000,192 |
| MiniMax M1 | $0.40 | $2.20 | — | 1,000,000 |
| MiniMax M2 | $0.255 | $1.00 | $0.03 | 196,608 |
| MiniMax M2.1 | $0.27 | $0.95 | $0.03 | 196,608 |
| MiniMax M2 Her | $0.30 | $1.20 | $0.03 | 65,536 |
| **MiniMax M2.5** | **$0.30** | **$1.10** | **$0.15** | **196,608** |

### 4.2 与竞品价格对比

- M2.5 output 价格仅为 Claude Opus 4.6 的 **1/10 ~ 1/20**
- 以 100 tokens/sec 速率持续运行1小时仅需 **$1**
- 以 50 tokens/sec 速率持续运行1小时仅需 **$0.30**
- 4个 M2.5 实例全年不间断运行仅需 **$10,000**

### 4.3 订阅计划

| 计划类型 | 说明 |
|----------|------|
| **Pay as You Go** | 按 token 计费，无最低消费 |
| **Coding Plan** | 开发者订阅，支持 M2.5/M2.1/M2 |
| **Audio Subscription** | 语音模型月度订阅，$5 ~ $999/月，额度 10万 ~ 2000万 credits |
| **Video Packages** | 视频生成资源包，$1,000 ~ $6,000/月，最高20%折扣 |

---

## 5. Benchmark 评测成绩

### 5.1 MiniMax M2.5（2026年2月，最新旗舰）

**编码能力：**

| Benchmark | M2.5 | Claude Opus 4.6 | 说明 |
|-----------|-------|-----------------|------|
| SWE-Bench Verified | **80.2%** | — | SOTA |
| Multi-SWE-Bench | **51.3%** | — | 多语言 SWE |
| SWE-Bench Verified (OpenCode) | 76.1% | 75.9% | 超越 Opus |
| SWE-Bench Verified (Droid) | 79.7% | 78.9% | 超越 Opus |
| VIBE-Pro | 与 Opus 4.5 持平 | — | 内部 benchmark |

**搜索与工具调用：**

| Benchmark | M2.5 |
|-----------|-------|
| BrowseComp（含 context management） | **76.3%** |
| Wide Search | 行业领先 |
| RISE（真实交互搜索评估） | 专家级表现 |

**综合能力（Benchable.ai 评测）：**

| 维度 | 准确率 | 百分位 |
|------|--------|--------|
| Coding | 93.0% | 83rd |
| Reasoning | 94.0% | 84th |
| General Knowledge & Ethics | 100% | — |
| Mathematics | 91.0% | 64th |
| Instruction Following | 65.0% | 68th |
| Hallucinations | 88.0% | 36th（弱项） |
| GPQA | 84.8% | — |

**效率指标：**
- SWE-Bench Verified 平均每任务消耗 3.52M tokens（M2.1 为 3.72M）
- 端到端运行时间：22.8分钟（M2.1 为 31.3分钟，提速 **37%**）
- 运行时间与 Claude Opus 4.6（22.9分钟）持平，但成本仅为其 **10%**
- 比 M2.1 减少约 **20%** 的搜索轮次

### 5.2 MiniMax M2 / M2.1

| Benchmark | M2 | M2.1 |
|-----------|-----|------|
| SWE-bench Verified | 69.4% | 74.0% |
| Multi-SWE-Bench | 36.2% | 49.4% |
| SWE-bench Multilingual | 56.5% | 72.5% |
| Terminal-Bench | 46.3% | — |
| BrowseComp | 44% | — |
| GAIA (text only) | 75.7% | — |
| τ²-Bench | 77.2% | — |
| MMLU | 82.0% | 87.5% |
| GPQA | 77.7% | 83.0% |
| Coding (LiveCodeBench) | 82.6% | 81.0% |

M2 在开源模型中综合评分全球排名 **#1**。

### 5.3 MiniMax M1（推理模型）

| Benchmark | M1 (80K) | M1 (40K) | DeepSeek R1 |
|-----------|----------|----------|-------------|
| AIME 2024 | **86.0%** | 83.3% | 79.8% |
| AIME 2025 | **76.9%** | 74.6% | — |
| LiveCodeBench | 65.0% | — | — |
| FullStackBench | 68.3% | — | — |
| GPQA Diamond | 70.0% | — | — |
| ZebraLogic | 86.8% | — | — |
| OpenAI-MRCR (1M tokens) | 56.2% | — | — |

### 5.4 MiniMax-01（基础模型）

- 性能与 GPT-4o 和 Claude-3.5-Sonnet 相当
- Context window 是上述模型的 **20~32倍**

---

## 6. 多模态产品矩阵

| 产品 | 版本 | 能力 |
|------|------|------|
| **文本模型** | M2.5 / M2.5-Lightning | 编码、Agent、办公、搜索 |
| **视频生成** | Hailuo 2.3（2025年10月） | 文生视频/图生视频，1080p，6~10秒，支持动漫/水墨/游戏CG风格 |
| **语音合成** | Speech 2.6 Turbo | TTS，支持32种语言，情感调节，零样本语音克隆 |
| **音乐生成** | Music 2.0 | 文本生成音乐 |
| **视频Agent** | Hailuo Video Agent（Beta） | 单击从文本/图片生成视频，三阶段演进 |
| **对话角色** | M2 Her | 角色扮演与情感对话 |

---

## 7. 开发者社区评价

### 7.1 正面评价

- **性价比极高**：output 价格仅为 Claude Opus 的 1/10~1/20，被称为"intelligence too cheap to meter"
- **写作场景**：Reddit 用户称 M2.5 为"真正的工作伙伴"，逻辑性强，事实核查准确率优于付费替代品
- **Agent 能力**：工具调用和搜索能力突出，BrowseComp 76.3% 行业领先
- **开源友好**：M2/M2.5 均已开源至 Hugging Face，支持本地部署
- **速度优势**：100 TPS 推理速度是其他前沿模型的约2倍
- **MiniMax 内部实践**：30% 的公司任务由 M2.5 自主完成，80% 的新代码由 M2.5 生成

### 7.2 负面评价与局限

- **幻觉问题**：Hallucinations benchmark 仅 88.0%（36th percentile），是明显弱项
- **复杂编码不稳定**：Reddit r/ChatGPTCoding 社区反馈，在复杂编码任务中出现严重幻觉，表现不如 GLM-5 和 Kimi k2.5
- **Instruction Following 一般**：65.0%（68th percentile）
- **Context Window 缩短**：M2 系列（~200K）相比 M1/MiniMax-01（1M）大幅缩短
- **本地部署门槛**：230B 总参数仍需多 GPU 服务器级硬件

### 7.3 社区总结

> M2.5 在 Agent/工具调用/搜索/写作场景表现出色，性价比无敌。但在复杂编码的一致性和幻觉控制方面仍有提升空间。适合作为高性价比的 Agent 基座模型，但对精度要求极高的场景建议搭配验证机制。

---

## 8. 关键数字速查

| 指标 | 数值 |
|------|------|
| M2.5 总参数 | 230B |
| M2.5 激活参数 | 10B |
| M2.5 Context Window | 204,800 tokens |
| M2.5 推理速度（Lightning） | 100 tokens/sec |
| M2.5 Input 价格 | $0.30 / 1M tokens |
| M2.5 Output 价格 | $1.10 / 1M tokens |
| M2.5 SWE-Bench Verified | 80.2% |
| M2.5 BrowseComp | 76.3% |
| M1 Context Window | 1,000,000 tokens |
| MiniMax-01 Context Window | 1,000,192 tokens（推理可达4M） |
| MiniMax-01 总参数 | 456B |
| 公司港股市值（首日） | ~HK$1,067亿（~$137亿） |
| RL 训练环境数量 | 200,000+ |
| 支持编程语言 | 10+（Go, C, C++, TypeScript, Rust, Kotlin, Python, Java, JavaScript, PHP, Lua, Dart, Ruby） |

---

## 9. 参考来源

- MiniMax 官方博客：https://minimax.io/news/minimax-m25
- Hugging Face 模型页：https://huggingface.co/MiniMaxAI/MiniMax-M2
- GitHub 开源仓库：https://github.com/MiniMax-AI/MiniMax-M2.5
- MiniMax-01 技术报告：https://arxiv.org/abs/2501.08313
- MiniMax-M1 技术报告：https://arxiv.org/abs/2506.13585
- API 定价页：https://platform.minimax.io/docs/pricing/overview
- 第三方定价追踪：https://pricepertoken.com/pricing-page/provider/minimax
- Benchable.ai 评测：https://benchable.ai/models/minimax/minimax-m2.5-20260211
- VentureBeat 报道：https://venturebeat.com/technology/minimaxs-new-open-m2-5-and-m2-5-lightning-near-state-of-the-art-while
- Reddit 社区讨论：r/ChatGPTCoding, r/WritingWithAI, r/LocalLLaMA
