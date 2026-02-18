<h1 align="center">🤖 AI Models for Vibe Coding</h1>

<p align="center">
  <b>Models we actually use — pricing, specs, benchmarks, and real-world feedback</b><br>
  <sub>Covering Anthropic, OpenAI, Google, Zhipu, Moonshot, MiniMax</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude-Opus_%7C_Sonnet-CC785C?logo=anthropic" alt="Claude"/>
  <img src="https://img.shields.io/badge/GPT-5.3_Codex-412991?logo=openai" alt="GPT"/>
  <img src="https://img.shields.io/badge/Gemini-3_Pro_%7C_Flash-4285F4?logo=google" alt="Gemini"/>
  <img src="https://img.shields.io/badge/GLM--5-Zhipu-00B4D8" alt="GLM-5"/>
  <img src="https://img.shields.io/badge/Kimi-K2.5-FF6B6B" alt="Kimi"/>
  <img src="https://img.shields.io/badge/MiniMax-M2.5-FFD700" alt="MiniMax"/>
</p>

---

<!-- ============================================================ -->
<!-- ENGLISH -->
<!-- ============================================================ -->

<details open>
<summary><h2>API Pricing</h2></summary>

| Model | Input ($/1M) | Output ($/1M) | Cache Write | Cache Read/Hit | Batch Input | Batch Output | Long Context | Notes |
|:------|:------------:|:-------------:|:-----------:|:--------------:|:-----------:|:------------:|:------------:|:------|
| **Claude Opus 4.6** | $5.00 | $25.00 | 5min: $6.25, 1h: $10.00 | $0.50 | $2.50 | $12.50 | >200K: $10/$37.50 | Fast Mode: $30/$150 |
| **Claude Sonnet 4.6** | $3.00 | $15.00 | 5min: $3.75, 1h: $6.00 | $0.30 | $1.50 | $7.50 | >200K: $6/$22.50 | — |
| **Claude Opus 4.5** | $5.00 | $25.00 | — | $0.50 | $2.50 | $12.50 | — | 67% cheaper than Opus 4.1 |
| **Claude Sonnet 4.5** | $3.00 | $15.00 | $3.75 | $0.30 | $1.50 | $7.50 | >200K: $6/$22.50 | — |
| **GPT-5.3 Codex** | $1.75 | $14.00 | — | Cached: $0.175 | — | — | — | Reasoning tokens billed as output |
| **GPT-5.3 Codex Spark** | — | — | — | — | — | — | — | Research Preview, no API pricing |
| **Gemini 3 Pro** | $2.00 | $12.00 | — | $0.20–0.40 | $1.00 | $6.00 | >200K: $4/$18 | Cache storage: $4.50/1M/hr |
| **Gemini 3 Flash** | $0.50 | $3.00 | — | $0.05 | — | — | — | Audio input: $1.00 |
| **GLM-5** | $1.00 | $3.20 | — | — | — | — | — | MIT open-source, self-deploy |
| **Kimi K2.5** | $0.60 | $3.00 | — | $0.10 | — | — | — | ~1/40 of Claude pricing |
| **MiniMax M2.5** | $0.30 | $1.10 | — | $0.15 | — | — | — | ~1/10–1/20 of Opus 4.6 |

> **Tip:** All prices are per 1 million tokens. "Cache Write" and "Cache Read/Hit" refer to prompt caching features. "Long Context" shows surcharges for inputs exceeding 200K tokens (format: input/output). Batch pricing applies to asynchronous batch API calls.

</details>

<!-- ============================================================ -->
<!-- CHINESE -->
<!-- ============================================================ -->

<details>
<summary><h2>API 定价</h2></summary>

| 模型 | 输入 ($/1M) | 输出 ($/1M) | Cache 写入 | Cache 读取 | Batch 输入 | Batch 输出 | 长上下文加价 | 备注 |
|:-----|:-----------:|:-----------:|:----------:|:----------:|:----------:|:----------:|:------------:|:-----|
| **Claude Opus 4.6** | $5.00 | $25.00 | 5min: $6.25, 1h: $10.00 | $0.50 | $2.50 | $12.50 | >200K: $10/$37.50 | Fast Mode: $30/$150 |
| **Claude Sonnet 4.6** | $3.00 | $15.00 | 5min: $3.75, 1h: $6.00 | $0.30 | $1.50 | $7.50 | >200K: $6/$22.50 | — |
| **Claude Opus 4.5** | $5.00 | $25.00 | — | $0.50 | $2.50 | $12.50 | — | 比 Opus 4.1 便宜 67% |
| **Claude Sonnet 4.5** | $3.00 | $15.00 | $3.75 | $0.30 | $1.50 | $7.50 | >200K: $6/$22.50 | — |
| **GPT-5.3 Codex** | $1.75 | $14.00 | — | 缓存: $0.175 | — | — | — | 推理 token 按输出计费 |
| **GPT-5.3 Codex Spark** | — | — | — | — | — | — | — | 研究预览版，暂无 API 定价 |
| **Gemini 3 Pro** | $2.00 | $12.00 | — | $0.20–0.40 | $1.00 | $6.00 | >200K: $4/$18 | 缓存存储: $4.50/1M/小时 |
| **Gemini 3 Flash** | $0.50 | $3.00 | — | $0.05 | — | — | — | 音频输入: $1.00 |
| **GLM-5** | $1.00 | $3.20 | — | — | — | — | — | MIT 开源，可自部署 |
| **Kimi K2.5** | $0.60 | $3.00 | — | $0.10 | — | — | — | 约为 Claude 定价的 1/40 |
| **MiniMax M2.5** | $0.30 | $1.10 | — | $0.15 | — | — | — | 约为 Opus 4.6 的 1/10–1/20 |

> **提示：** 所有价格均为每百万 token。"Cache 写入"和"Cache 读取"指提示缓存功能。"长上下文加价"为超过 200K token 输入时的附加费用（格式：输入/输出）。Batch 定价适用于异步批量 API 调用。

</details>
<!-- ENGLISH -->

## Subscription Plans & Limits

This section details the subscription tiers, pricing, and request limits for each major AI provider. Plans and pricing are subject to change; refer to each provider's official page for the latest information.

---

### Claude (Anthropic)

| Plan | Price | Opus Access | Limits | Notes |
|------|-------|-------------|--------|-------|
| Free | $0 | ❌ Sonnet only | Limited, resets every 5h | — |
| Pro | $20/mo ($17/mo annual) | ✅ Limited | ~45 msgs/5h rolling | Memory, Research, Claude Code |
| Max 5x | $100/mo | ✅ Full, high priority | 5× Pro | Early access to new features |
| Max 20x | $200/mo | ✅ Full, top priority | 20× Pro, zero-latency | — |
| Team (Standard) | $25/mo ($20 annual) | ✅ | 5–150 users | SSO, admin console |
| Team (Advanced) | $125/mo ($100 annual) | ✅ | 5× Standard | — |
| Enterprise | Custom | ✅ | Custom | HIPAA, SCIM, audit logs |

**Key details:**

- **Free** users can only access Sonnet; Opus is not available. Usage is limited and resets on a rolling 5-hour window.
- **Pro** subscribers get limited Opus access with approximately 45 messages per 5-hour rolling window. Includes Memory (persistent context across conversations), Research (deep web research), and Claude Code (CLI-based agentic coding tool).
- **Max 5x** provides 5 times the Pro usage limits with full Opus access at high priority, plus early access to newly released features.
- **Max 20x** provides 20 times the Pro usage limits with top-priority Opus access and zero-latency queuing.
- **Team (Standard)** is designed for small-to-medium teams (5–150 users) with SSO and an admin console for user management.
- **Team (Advanced)** offers 5 times the Standard usage limits for teams with heavier workloads.
- **Enterprise** provides custom pricing and limits, with compliance features including HIPAA, SCIM provisioning, and audit logs.

---

### ChatGPT / Codex (OpenAI)

#### ChatGPT Plans

| Plan | Price | Key Features |
|------|-------|--------------|
| Free | $0 | Limited GPT-5.2 |
| Go | $8/mo | Extended GPT-5.2 Instant |
| Plus | $20/mo | Codex agent, advanced reasoning, Sora |
| Pro | $200/mo | Unlimited GPT-5.2, Spark preview, extended Codex |
| Business | $25–30/user/mo | Unlimited messages, SAML SSO, 60+ integrations |
| Enterprise | Custom | Extended context, data residency (10 regions), 24/7 support |

**Key details:**

- **Free** users get limited access to GPT-5.2 with lower rate limits and no access to advanced features.
- **Go** is a lightweight tier offering extended access to GPT-5.2 Instant (the faster, lower-latency variant) at a budget-friendly price.
- **Plus** unlocks the Codex agent (cloud-based autonomous coding), advanced reasoning modes, and Sora (video generation).
- **Pro** removes most usage caps on GPT-5.2, provides a preview of Spark (next-generation reasoning), and extends Codex cloud task limits significantly.
- **Business** is per-user pricing for organizations, with unlimited messages, SAML SSO, and 60+ third-party integrations.
- **Enterprise** offers custom pricing with extended context windows, data residency across 10 global regions, and dedicated 24/7 support.

#### Codex Limits (per 5-hour rolling window)

| Plan | Local Messages | Cloud Tasks | Code Reviews/week |
|------|---------------|-------------|-------------------|
| Plus | 45–225 | 10–60 | 10–25 |
| Pro | 300–1,500 | 50–400 | 100–250 |

**Key details:**

- **Local Messages** refer to in-editor Codex interactions (inline completions, chat-based edits).
- **Cloud Tasks** are autonomous background tasks where Codex works on a sandboxed cloud environment (e.g., implementing a feature, fixing a bug across multiple files).
- **Code Reviews/week** is the number of automated pull request reviews Codex can perform per week.
- Limits are expressed as ranges because OpenAI dynamically adjusts them based on system load and demand.

---

### Google AI

#### Consumer Plans

| Plan | Price | Credits | Key Benefits |
|------|-------|---------|--------------|
| Free | $0 | 50/day | Gemini 3 Flash limited |
| AI Plus | $7.99/mo (promo $3.99×2mo) | 200/mo | Gemini 3 Pro, Veo 3, 200GB |
| AI Pro | $19.99/mo (first month free) | 1,000/mo | Higher Pro quota, students free 1yr |
| AI Ultra | $250/mo | — | Deep Think, Veo 3 early, Imagen 4, 30TB, YouTube Premium |

**Key details:**

- **Free** users receive 50 credits per day, sufficient for basic Gemini 3 Flash interactions. Access to Pro models is not included.
- **AI Plus** provides 200 credits per month with access to Gemini 3 Pro, Veo 3 (video generation), and 200GB of Google One storage. A promotional price of $3.99/mo is available for the first 2 months.
- **AI Pro** provides 1,000 credits per month with higher Gemini 3 Pro quotas. The first month is free. Students can get AI Pro free for 1 year with a valid .edu email.
- **AI Ultra** is the premium tier with unlimited-style access, including Deep Think (extended reasoning), early access to Veo 3, Imagen 4 (image generation), 30TB of Google One storage, and YouTube Premium included.

#### API Rate Limits

| Tier | RPM | TPM | RPD |
|------|-----|-----|-----|
| Free | 5–10 | 250K | 100 |
| Tier 1 | 150–300 | 1–2M | 1K–10K |
| Tier 2 | 500–2,000 | 2M | 10K+ |

**Key details:**

- **RPM** = Requests Per Minute, **TPM** = Tokens Per Minute, **RPD** = Requests Per Day.
- **Free** API tier is suitable for prototyping and experimentation with very low rate limits.
- **Tier 1** is the standard paid tier, suitable for small-to-medium production workloads.
- **Tier 2** is for high-volume production use cases with significantly higher throughput allowances.
- Tier upgrades are typically automatic based on usage history and billing account standing.

---

### GLM-5 (Zhipu / Z.ai)

| Access Method | Details |
|---------------|---------|
| API Pricing | $1 per 1M input tokens / $3.20 per 1M output tokens |
| chat.z.ai | Free chat interface, no registration required |
| Self-Deploy (HuggingFace) | Full model weights available on HuggingFace under MIT license |
| Self-Deploy (ModelScope) | Full model weights available on ModelScope under MIT license |
| NVIDIA NIM | Free tier available via NVIDIA NIM for optimized inference |

**Key details:**

- GLM-5 is fully open-weight under the MIT license, meaning there are no subscription tiers — you can self-host without restrictions.
- The API pricing of $1/$3.20 per 1M tokens (input/output) is competitive and pay-as-you-go with no minimum commitment.
- **chat.z.ai** provides a free, no-registration web chat interface for casual use and evaluation.
- Self-deployment is supported on both HuggingFace and ModelScope, with community-maintained quantized variants available.
- **NVIDIA NIM** offers a free tier for deploying GLM-5 with optimized inference on NVIDIA hardware.

---

### Kimi K2.5 (Moonshot AI)

#### Consumer Plans

| Plan | Price | Limits |
|------|-------|--------|
| Free | $0 | ~1.5M tokens/day (varies by region) |
| Starter | $5.99/mo | 250 conversations/mo |
| Pro | $12.99/mo | 600 conversations/mo |
| Premium | $19.99/mo | 1,000 conversations/mo |

#### API Access

| Access Method | Details |
|---------------|---------|
| Free Tier | ~1.5M tokens/day |
| SDK Compatibility | OpenAI SDK compatible (drop-in replacement) |

**Key details:**

- **Free** users get approximately 1.5 million tokens per day, though the exact limit varies by region and demand.
- **Starter**, **Pro**, and **Premium** plans are conversation-based rather than token-based, making usage more predictable for chat-heavy workflows.
- The API free tier also provides approximately 1.5M tokens/day, suitable for prototyping and light production use.
- Kimi K2.5's API is fully compatible with the OpenAI SDK, allowing developers to switch by changing only the base URL and API key.

---

### MiniMax

| Plan | Details |
|------|---------|
| Pay as You Go | Per-token pricing, no minimum spend or commitment |
| Coding Plan | Developer subscription for M2.5 / M2.1 / M2 model access |
| Audio Subscription | $5–$999/mo (tiered by usage volume) |

**Key details:**

- **Pay as You Go** is the default billing model — you pay per token consumed with no minimum spend, making it ideal for variable workloads.
- **Coding Plan** is a developer-focused subscription that provides dedicated access to MiniMax's coding-optimized models (M2.5, M2.1, M2) with higher rate limits and priority queuing.
- **Audio Subscription** ranges from $5/mo to $999/mo depending on usage volume, covering text-to-speech, speech-to-text, and voice cloning capabilities.

---

<!-- CHINESE -->

## 订阅计划与请求限制

本节详细介绍各主要 AI 服务商的订阅层级、定价和请求限制。计划和定价可能随时变动，请参阅各服务商官方页面获取最新信息。

---

### Claude（Anthropic）

| 计划 | 价格 | Opus 访问权限 | 限制 | 备注 |
|------|------|--------------|------|------|
| Free（免费版） | $0 | ❌ 仅限 Sonnet | 有限额度，每 5 小时重置 | — |
| Pro | $20/月（$17/月，按年付费） | ✅ 有限 | 约 45 条消息/5 小时滚动窗口 | Memory、Research、Claude Code |
| Max 5x | $100/月 | ✅ 完整访问，高优先级 | 5 倍 Pro 额度 | 新功能抢先体验 |
| Max 20x | $200/月 | ✅ 完整访问，最高优先级 | 20 倍 Pro 额度，零延迟 | — |
| Team（Standard） | $25/月（$20，按年付费） | ✅ | 5–150 名用户 | SSO、管理控制台 |
| Team（Advanced） | $125/月（$100，按年付费） | ✅ | 5 倍 Standard 额度 | — |
| Enterprise（企业版） | 定制价格 | ✅ | 定制额度 | HIPAA、SCIM、审计日志 |

**详细说明：**

- **Free（免费版）** 用户仅可使用 Sonnet 模型，无法访问 Opus。使用额度有限，按 5 小时滚动窗口重置。
- **Pro** 订阅者可有限访问 Opus，约每 5 小时滚动窗口内可发送 45 条消息。包含 Memory（跨对话持久化上下文）、Research（深度网络研究）和 Claude Code（基于命令行的智能编程工具）。
- **Max 5x** 提供 5 倍于 Pro 的使用额度，完整 Opus 访问权限且享有高优先级，并可抢先体验新发布的功能。
- **Max 20x** 提供 20 倍于 Pro 的使用额度，最高优先级 Opus 访问权限，零延迟排队。
- **Team（Standard）** 面向中小型团队（5–150 名用户），提供 SSO 和管理控制台进行用户管理。
- **Team（Advanced）** 提供 5 倍于 Standard 的使用额度，适合工作负载较重的团队。
- **Enterprise（企业版）** 提供定制价格和额度，合规功能包括 HIPAA、SCIM 自动配置和审计日志。

---

### ChatGPT / Codex（OpenAI）

#### ChatGPT 计划

| 计划 | 价格 | 主要功能 |
|------|------|----------|
| Free（免费版） | $0 | 有限的 GPT-5.2 访问 |
| Go | $8/月 | 扩展的 GPT-5.2 Instant |
| Plus | $20/月 | Codex 智能体、高级推理、Sora |
| Pro | $200/月 | 无限 GPT-5.2、Spark 预览、扩展 Codex |
| Business（商业版） | $25–30/用户/月 | 无限消息、SAML SSO、60+ 集成 |
| Enterprise（企业版） | 定制价格 | 扩展上下文、数据驻留（10 个区域）、7×24 支持 |

**详细说明：**

- **Free（免费版）** 用户可有限访问 GPT-5.2，速率限制较低，无法使用高级功能。
- **Go** 是轻量级层级，以实惠的价格提供扩展的 GPT-5.2 Instant（更快、更低延迟的变体）访问。
- **Plus** 解锁 Codex 智能体（基于云的自主编程）、高级推理模式和 Sora（视频生成）。
- **Pro** 移除 GPT-5.2 的大部分使用上限，提供 Spark（下一代推理）预览，并显著扩展 Codex 云任务限制。
- **Business（商业版）** 按用户计费，面向组织，提供无限消息、SAML SSO 和 60+ 第三方集成。
- **Enterprise（企业版）** 提供定制价格，扩展上下文窗口，支持 10 个全球区域的数据驻留，以及专属 7×24 支持。

#### Codex 限制（每 5 小时滚动窗口）

| 计划 | 本地消息 | 云端任务 | 代码审查/周 |
|------|----------|----------|-------------|
| Plus | 45–225 | 10–60 | 10–25 |
| Pro | 300–1,500 | 50–400 | 100–250 |

**详细说明：**

- **本地消息** 指编辑器内的 Codex 交互（内联补全、基于聊天的编辑）。
- **云端任务** 是 Codex 在沙盒云环境中执行的自主后台任务（例如实现功能、跨多个文件修复 Bug）。
- **代码审查/周** 是 Codex 每周可执行的自动 Pull Request 审查数量。
- 限制以范围形式表示，因为 OpenAI 会根据系统负载和需求动态调整。

---

### Google AI

#### 消费者计划

| 计划 | 价格 | 积分 | 主要权益 |
|------|------|------|----------|
| Free（免费版） | $0 | 50/天 | Gemini 3 Flash 有限访问 |
| AI Plus | $7.99/月（促销价 $3.99×2 个月） | 200/月 | Gemini 3 Pro、Veo 3、200GB 存储 |
| AI Pro | $19.99/月（首月免费） | 1,000/月 | 更高 Pro 配额，学生免费 1 年 |
| AI Ultra | $250/月 | — | Deep Think、Veo 3 抢先体验、Imagen 4、30TB 存储、YouTube Premium |

**详细说明：**

- **Free（免费版）** 用户每天获得 50 积分，足够基本的 Gemini 3 Flash 交互使用。不包含 Pro 模型访问权限。
- **AI Plus** 每月提供 200 积分，可访问 Gemini 3 Pro、Veo 3（视频生成）和 200GB Google One 存储空间。前 2 个月可享受 $3.99/月的促销价。
- **AI Pro** 每月提供 1,000 积分，Gemini 3 Pro 配额更高。首月免费。学生凭有效 .edu 邮箱可免费使用 AI Pro 1 年。
- **AI Ultra** 是高级层级，提供无限制式访问，包括 Deep Think（扩展推理）、Veo 3 抢先体验、Imagen 4（图像生成）、30TB Google One 存储空间，以及 YouTube Premium。

#### API 速率限制

| 层级 | RPM（每分钟请求数） | TPM（每分钟 Token 数） | RPD（每日请求数） |
|------|---------------------|------------------------|-------------------|
| Free（免费） | 5–10 | 250K | 100 |
| Tier 1 | 150–300 | 1–2M | 1K–10K |
| Tier 2 | 500–2,000 | 2M | 10K+ |

**详细说明：**

- **RPM** = 每分钟请求数，**TPM** = 每分钟 Token 数，**RPD** = 每日请求数。
- **Free（免费）** API 层级适合原型开发和实验，速率限制非常低。
- **Tier 1** 是标准付费层级，适合中小型生产工作负载。
- **Tier 2** 面向高流量生产场景，吞吐量配额显著提高。
- 层级升级通常根据使用历史和账单账户状态自动进行。

---

### GLM-5（智谱 / Z.ai）

| 访问方式 | 详情 |
|----------|------|
| API 定价 | 输入 $1 / 输出 $3.20（每百万 Token） |
| chat.z.ai | 免费聊天界面，无需注册 |
| 自部署（HuggingFace） | 完整模型权重，MIT 许可证 |
| 自部署（ModelScope） | 完整模型权重，MIT 许可证 |
| NVIDIA NIM | 免费层级，优化推理 |

**详细说明：**

- GLM-5 采用 MIT 许可证完全开源开放权重，没有订阅层级之分——您可以无限制地自行部署。
- API 定价为输入 $1 / 输出 $3.20（每百万 Token），具有竞争力，按量付费，无最低消费。
- **chat.z.ai** 提供免费、无需注册的网页聊天界面，适合日常使用和模型评估。
- 支持在 HuggingFace 和 ModelScope 上自部署，社区维护的量化版本也可获取。
- **NVIDIA NIM** 提供免费层级，可在 NVIDIA 硬件上以优化推理方式部署 GLM-5。

---

### Kimi K2.5（月之暗面 / Moonshot AI）

#### 消费者计划

| 计划 | 价格 | 限制 |
|------|------|------|
| Free（免费版） | $0 | 约 150 万 Token/天（因地区而异） |
| Starter | $5.99/月 | 250 次对话/月 |
| Pro | $12.99/月 | 600 次对话/月 |
| Premium | $19.99/月 | 1,000 次对话/月 |

#### API 访问

| 访问方式 | 详情 |
|----------|------|
| 免费层级 | 约 150 万 Token/天 |
| SDK 兼容性 | 兼容 OpenAI SDK（可直接替换） |

**详细说明：**

- **Free（免费版）** 用户每天可获得约 150 万 Token，但具体限制因地区和需求而异。
- **Starter**、**Pro** 和 **Premium** 计划基于对话次数而非 Token 数计费，使聊天密集型工作流的使用量更可预测。
- API 免费层级同样提供约每天 150 万 Token，适合原型开发和轻量级生产使用。
- Kimi K2.5 的 API 完全兼容 OpenAI SDK，开发者只需更改 base URL 和 API key 即可切换。

---

### MiniMax

| 计划 | 详情 |
|------|------|
| Pay as You Go（按量付费） | 按 Token 计费，无最低消费或承诺 |
| Coding Plan（编程计划） | 面向开发者的订阅，可访问 M2.5 / M2.1 / M2 模型 |
| Audio Subscription（音频订阅） | $5–$999/月（按使用量分层） |

**详细说明：**

- **Pay as You Go（按量付费）** 是默认计费模式——按消耗的 Token 付费，无最低消费，非常适合工作负载不稳定的场景。
- **Coding Plan（编程计划）** 是面向开发者的订阅，提供对 MiniMax 编程优化模型（M2.5、M2.1、M2）的专属访问，享有更高速率限制和优先排队。
- **Audio Subscription（音频订阅）** 根据使用量从 $5/月到 $999/月不等，涵盖文本转语音、语音转文本和语音克隆功能。
<!-- ENGLISH -->

## Model Specifications

| Model | Release | Context | Max Output | Thinking / Reasoning | Multimodal | Architecture | Speed |
|-------|---------|---------|------------|----------------------|------------|--------------|-------|
| Claude Opus 4.6 | 2026-02-05 | 200K (1M beta) | 128K | Adaptive: low/medium/high/max | Text + Image | — | — |
| Claude Sonnet 4.6 | 2026-02-17 | 200K (1M beta) | 64K | Adaptive + Extended Thinking | Text + Image | — | — |
| Claude Opus 4.5 | 2025-11-24 | 200K (1M beta) | 64K | Extended Thinking, effort adjustable | Text + Image | — | — |
| Claude Sonnet 4.5 | 2025-09-29 | 200K (1M beta) | 64K | Extended Thinking | Text + Image | — | — |
| GPT-5.3 Codex | 2026-02-05 | 400K | 128K | Reasoning effort: low/medium/high | Text + Image | — | ~65–70 tok/s |
| GPT-5.3 Codex Spark | 2026-02-12 | 128K | — | Lightweight reasoning | Text only | Cerebras WSE-3 | 1,000+ tok/s |
| Gemini 3 Pro | 2025-11-18 | 1M | 64K | Dynamic Thinking (LOW/HIGH), always-on | Text + Image + Audio + Video + PDF | MoE Transformer | — |
| Gemini 3 Flash | 2025-12-17 | 1M | 64K | Dynamic Thinking (minimal/low/medium/high) | Text + Image + Video + Audio + PDF | — | ~218 tok/s |
| GLM-5 | 2026-02-11 | 200K | 128K | Reasoning mode (optional) | Text | 744B MoE (44B active), 256 experts, Ascend 910B | ~17–19 tok/s |
| Kimi K2.5 | 2026-01-27 | 256K | 8K | Thinking / Instant dual mode | Text + Image + Video + PDF | 1T MoE (32B active), 384 experts | — |
| MiniMax M2.5 | 2026-02-12 | ~205K | Long (w/ CoT) | Reasoning optimized | Text | 230B MoE (10B active) | Standard ~50 tok/s, Lightning ~100 tok/s |

### Key Highlights

- **Gemini 3 Pro / Flash** offer the largest context window at **1M tokens**, with always-on Dynamic Thinking and the broadest multimodal support (text, image, audio, video, PDF).
- **GPT-5.3 Codex Spark** achieves **1,000+ tok/s** inference speed by running on Cerebras WSE-3 wafer-scale hardware — an order of magnitude faster than any other model listed.
- **GLM-5** is the only model released under an **MIT open-source license**, built on a 744B MoE architecture running natively on Huawei **Ascend 910B** chips.
- **Kimi K2.5** fields the largest total parameter count at **1 trillion** (32B active) with 384 experts, while keeping its active footprint small for efficient serving.
- **Claude Opus 4.6** leads on max output length at **128K tokens** (tied with GPT-5.3 Codex and GLM-5), paired with a new adaptive thinking system offering four granularity levels.

---

<!-- CHINESE -->

## 模型规格对比

| 模型 | 发布日期 | 上下文窗口 | 最大输出 | 推理/思考 | 多模态 | 架构 | 速度 |
|------|----------|------------|----------|-----------|--------|------|------|
| Claude Opus 4.6 | 2026-02-05 | 200K（1M 内测） | 128K | 自适应：low/medium/high/max | 文本 + 图像 | — | — |
| Claude Sonnet 4.6 | 2026-02-17 | 200K（1M 内测） | 64K | 自适应 + 扩展思考 | 文本 + 图像 | — | — |
| Claude Opus 4.5 | 2025-11-24 | 200K（1M 内测） | 64K | 扩展思考，可调节推理力度 | 文本 + 图像 | — | — |
| Claude Sonnet 4.5 | 2025-09-29 | 200K（1M 内测） | 64K | 扩展思考 | 文本 + 图像 | — | — |
| GPT-5.3 Codex | 2026-02-05 | 400K | 128K | 推理力度：low/medium/high | 文本 + 图像 | — | ~65–70 tok/s |
| GPT-5.3 Codex Spark | 2026-02-12 | 128K | — | 轻量推理 | 仅文本 | Cerebras WSE-3 | 1,000+ tok/s |
| Gemini 3 Pro | 2025-11-18 | 1M | 64K | 动态思考（LOW/HIGH），始终开启 | 文本 + 图像 + 音频 + 视频 + PDF | MoE Transformer | — |
| Gemini 3 Flash | 2025-12-17 | 1M | 64K | 动态思考（minimal/low/medium/high） | 文本 + 图像 + 视频 + 音频 + PDF | — | ~218 tok/s |
| GLM-5 | 2026-02-11 | 200K | 128K | 推理模式（可选） | 文本 | 744B MoE（44B 激活），256 专家，昇腾 910B | ~17–19 tok/s |
| Kimi K2.5 | 2026-01-27 | 256K | 8K | 思考/即时 双模式 | 文本 + 图像 + 视频 + PDF | 1T MoE（32B 激活），384 专家 | — |
| MiniMax M2.5 | 2026-02-12 | ~205K | 长输出（含 CoT） | 推理优化 | 文本 | 230B MoE（10B 激活） | 标准 ~50 tok/s，闪电 ~100 tok/s |

### 亮点速览

- **Gemini 3 Pro / Flash** 拥有最大的 **100 万 token** 上下文窗口，动态思考始终开启，并支持最广泛的多模态输入（文本、图像、音频、视频、PDF）。
- **GPT-5.3 Codex Spark** 基于 Cerebras WSE-3 晶圆级硬件，推理速度达到 **1,000+ tok/s**，比列表中其他模型快一个数量级。
- **GLM-5** 是唯一以 **MIT 开源协议** 发布的模型，采用 744B MoE 架构，原生运行于华为**昇腾 910B** 芯片。
- **Kimi K2.5** 总参数量达 **1 万亿**（32B 激活），拥有 384 个专家，在保持高效推理的同时实现了最大的模型规模。
- **Claude Opus 4.6** 最大输出长度达 **128K token**（与 GPT-5.3 Codex 和 GLM-5 并列），并引入四档自适应思考系统。
<!-- ENGLISH -->

## Benchmarks

### Coding & Software Engineering

| Benchmark | Opus 4.6 | Sonnet 4.6 | Opus 4.5 | Sonnet 4.5 | GPT-5.3 Codex | Gemini 3 Pro | Gemini 3 Flash | GLM-5 | Kimi 2.5 | MiniMax M2.5 |
|-----------|----------|------------|----------|------------|---------------|-------------|----------------|-------|----------|--------------|
| SWE-bench Verified | 80.8% | 79.6% | **80.9%** | 77.2% | — | 76.2% | 78.0% | 77.8% | 76.8% | **80.2%** |
| Terminal-Bench 2.0 | 65.4% | — | 59.8% | 50.0% | **77.3%** | 56.2% | — | 56.2% | 50.8% | — |
| OSWorld | — | **72.5%** | 66.3% | 61.4% | 64.7% | — | — | — | — | — |
| LiveCodeBench | — | — | — | — | — | — | **90.8%** | — | 85.0% | — |

### Reasoning & Knowledge

| Benchmark | Opus 4.6 | Sonnet 4.6 | GPT-5.3 Codex | Gemini 3 Pro | Gemini 3 Flash | GLM-5 | Kimi 2.5 |
|-----------|----------|------------|---------------|-------------|----------------|-------|----------|
| GPQA Diamond | ~77% | 89.9% | 73.8% | **91.9%** | 90.4% | 68–86% | 87.6% |
| MMLU / MMLU-Pro | 85.1% | 89.3% | — | **92%** | — | — | 87.1% |
| ARC-AGI-2 | **68.8%** | 58.3% | — | 31–45% | 33.6% | — | — |
| Humanity's Last Exam | 40–53% | 33–49% | — | 38–46% | 33.7% | **50.4%** | **50.2%** |
| AIME 2025 | ~94% | — | — | 95–100% | **99.7%** | 88.7% | 96.1% |

### Analysis

On **SWE-bench Verified**, Opus 4.5 (80.9%), Opus 4.6 (80.8%), and MiniMax M2.5 (80.2%) form the top tier at ~80%, while Gemini 3 Flash (78.0%) surprisingly outperforms Gemini 3 Pro (76.2%). **Terminal-Bench 2.0** is dominated by GPT-5.3 Codex at 77.3%, a full 12 points ahead of the next competitor. In **reasoning**, the landscape fragments: Opus 4.6 leads ARC-AGI-2 at 68.8% (nearly doubling its predecessor); Gemini 3 Pro tops GPQA Diamond (91.9%) and MMLU (92%); GLM-5 and Kimi K2.5 share the lead on Humanity's Last Exam (~50%). For **long context**, Opus 4.6 achieves ~76% on MRCR v2 at 1M tokens, while the Gemini 3 series offers 1M context natively across both Pro and Flash.

---

## User Reviews

### Claude Opus 4.6

- 👍 "Like a senior engineer handling million-line codebase migrations" — SentinelOne. ARC-AGI-2 score nearly doubled from 4.5. The 1M context beta fundamentally changes how teams approach large-repo refactors and cross-file reasoning.
- 👎 Writing quality described as "flatter" than Opus 4.5 — less creative prose, more mechanical output. Overconfident behavior: executes destructive actions without confirmation. Pro users report hitting rate limits within 2–3 hours of heavy use. An API regression incident on Feb 10–11 caused widespread disruption.

### Claude Sonnet 4.6

- 👍 "Opus 4.5 at Sonnet pricing" — Reddit consensus. 70% preferred over Sonnet 4.5 in Claude Code internal testing. OSWorld score of 72.5% is the highest among all models tested.
- 👎 Complex multi-step tasks still require Opus-tier models. Some developers report higher token consumption in the 4.6 series compared to 4.5, partially offsetting cost savings.

### Claude Opus 4.5

- 👍 First model to break 80% on SWE-bench Verified. "It just gets it" for architecture patterns and large-scale refactoring — Reddit r/ClaudeCode. Token efficiency is best-in-class among frontier models.
- 👎 Over-autonomous tendencies: rewrites entire architecture without asking, over-documents code with excessive comments. Users report "memory anxiety" as the model approaches thinking token limits, leading to rushed or truncated outputs.

### Claude Sonnet 4.5

- 👍 Replit reported code edit error rate dropped from 9% to 0% after switching. "Like pairing with a senior engineer" — Skywork AI. Strong balance of speed and quality for everyday coding tasks.
- 👎 "Confidently lies about having read the docs" — Reddit r/cursor. Weak long-context retrieval: only 18.5% accuracy at 256K tokens. Many users feel it is "not a huge upgrade" over Sonnet 4, especially for non-coding tasks.

### GPT-5.3 Codex

- 👍 "Start a task, leave for hours, come back to working software" — Matt Shumer. Terminal-Bench #1 at 77.3%. Community consensus: use Opus for planning and architecture, Codex for parallel execution of well-defined tasks.
- 👎 Silent routing to GPT-5.2 reported by multiple users during peak hours. Spark mode: "rarely logic errors but adds junk code and unnecessary abstractions." One user spent $100 on Opus credits specifically to clean up a Codex-generated dashboard.

### Gemini 3 Pro

- 👍 Initially hailed as "clearly superior to GPT-5.2 and Opus 4.5" — Reddit. GPQA Diamond 91.9% is the highest single-model score. Scaffolding, refactoring, and structured output praised by enterprise users.
- 👎 Long context quality degrades noticeably after 50K tokens despite 1M window. Rate limits slashed post-launch (RPM −67%, RPD −80%). "API frequently becomes unavailable during US business hours." Hallucinations on niche or domain-specific topics remain a concern.

### Gemini 3 Flash

- 👍 "The Budget Model That Became My Default" — popular blog post title. 218 tok/s output speed, 1.7× faster than GPT-5.2. SWE-bench 78.0% beats Gemini 3 Pro (76.2%), a rare case of a smaller model outperforming its larger sibling on agentic coding.
- 👎 Hallucination rate measured at ~91% on Vectara benchmark. Free-tier quota slashed from 250 to 20 RPD. "Cannot stop outputting code comments" — developers report excessive inline documentation that inflates token usage.

### GLM-5

- 👍 Humanity's Last Exam 50.4% beats GPT-5.2 and Opus 4.5. Hallucination rate of 34% is the industry lowest on Vectara benchmark. "Lightyears better than GLM-4.7" — Reddit. Fully MIT open-source with zero NVIDIA dependency (runs on Ascend NPUs).
- 👎 Slow inference at 17–19 tok/s. Agent-mode coding still lags behind closed-source models on complex multi-file tasks. Requires more precise and structured prompts than Claude to achieve best results.

### Kimi K2.5

- 👍 Visual coding workflow praised — screenshot or screencast to working code. OCRBench 92.3% is the highest among all models. Agent Swarm supports up to 100 concurrent agents. Pricing at ~1/40 of Claude makes it accessible for high-volume use.
- 👎 "Wrote code with it for a week, verdict: not good" — V2EX user review. 0% output consistency at temperature=0 (determinism issues). Logic confusion reported: one user's agent accidentally git-rolled back an entire codebase. Inference speed is slow for interactive use.

### MiniMax M2.5

- 👍 SWE-bench Verified 80.2% — SOTA among non-Anthropic models. "Intelligence too cheap to meter" — output pricing at $1.10/1M tokens. Lightning mode at 100 tok/s. MiniMax reports 30% of internal company tasks now handled by M2.5.
- 👎 Hallucination benchmark score of 88% places it at the 36th percentile. Complex coding tasks show inconsistency across runs. Instruction following at 65% (68th percentile) means it occasionally ignores constraints or formatting requirements.

---

## Selection Guide

| Use Case | Recommended Models |
|----------|-------------------|
| Long context + deep reasoning | Claude Opus 4.6 (1M beta), Gemini 3 Pro |
| Coding + agent execution | GPT-5.3 Codex, Claude Opus 4.6, MiniMax M2.5 |
| Cost-effective coding | Gemini 3 Flash, Sonnet 4.6, GLM-5, MiniMax M2.5 |
| Fast iteration / frontend | GPT-5.3 Codex Spark, Kimi K2.5 (visual coding) |
| Open-source / self-deploy | GLM-5, Kimi K2.5, MiniMax M2.5 |
| Document / OCR / multimodal | Kimi K2.5, Gemini 3 series |

## Notes

- Pricing and quotas are subject to change; always check official documentation for the latest information.
- Benchmark scores vary by evaluation setup, including pass@k settings, tool availability, and thinking budget levels.
- User reviews sourced from Reddit, Hacker News, 知乎, V2EX, and 掘金 — these reflect subjective individual experiences and may not generalize.

---

<!-- CHINESE -->

## 基准测试性能

### 编程与软件工程

| 基准测试 | Opus 4.6 | Sonnet 4.6 | Opus 4.5 | Sonnet 4.5 | GPT-5.3 Codex | Gemini 3 Pro | Gemini 3 Flash | GLM-5 | Kimi 2.5 | MiniMax M2.5 |
|---------|----------|------------|----------|------------|---------------|-------------|----------------|-------|----------|--------------|
| SWE-bench Verified | 80.8% | 79.6% | **80.9%** | 77.2% | — | 76.2% | 78.0% | 77.8% | 76.8% | **80.2%** |
| Terminal-Bench 2.0 | 65.4% | — | 59.8% | 50.0% | **77.3%** | 56.2% | — | 56.2% | 50.8% | — |
| OSWorld | — | **72.5%** | 66.3% | 61.4% | 64.7% | — | — | — | — | — |
| LiveCodeBench | — | — | — | — | — | — | **90.8%** | — | 85.0% | — |

### 推理与知识

| 基准测试 | Opus 4.6 | Sonnet 4.6 | GPT-5.3 Codex | Gemini 3 Pro | Gemini 3 Flash | GLM-5 | Kimi 2.5 |
|---------|----------|------------|---------------|-------------|----------------|-------|----------|
| GPQA Diamond | ~77% | 89.9% | 73.8% | **91.9%** | 90.4% | 68–86% | 87.6% |
| MMLU / MMLU-Pro | 85.1% | 89.3% | — | **92%** | — | — | 87.1% |
| ARC-AGI-2 | **68.8%** | 58.3% | — | 31–45% | 33.6% | — | — |
| Humanity's Last Exam | 40–53% | 33–49% | — | 38–46% | 33.7% | **50.4%** | **50.2%** |
| AIME 2025 | ~94% | — | — | 95–100% | **99.7%** | 88.7% | 96.1% |

### 分析

在 **SWE-bench Verified** 上，Opus 4.5（80.9%）、Opus 4.6（80.8%）和 MiniMax M2.5（80.2%）组成了约 80% 的第一梯队，而 Gemini 3 Flash（78.0%）出人意料地超过了 Gemini 3 Pro（76.2%）。**Terminal-Bench 2.0** 由 GPT-5.3 Codex 以 77.3% 的成绩一骑绝尘，领先第二名 12 个百分点。在**推理**方面，格局呈现碎片化：Opus 4.6 以 68.8% 领跑 ARC-AGI-2（几乎是前代的两倍）；Gemini 3 Pro 在 GPQA Diamond（91.9%）和 MMLU（92%）上居首；GLM-5 和 Kimi K2.5 在 Humanity's Last Exam 上并列领先（约 50%）。在**长上下文**方面，Opus 4.6 在 1M token 的 MRCR v2 上达到约 76%，而 Gemini 3 系列在 Pro 和 Flash 上均原生支持 1M 上下文。

---

## 用户评价与社区反馈

### Claude Opus 4.6

- 👍 "就像一位资深工程师在处理百万行代码库的迁移" — SentinelOne。ARC-AGI-2 得分相比 4.5 几乎翻倍。1M 上下文 beta 从根本上改变了团队处理大型仓库重构和跨文件推理的方式。
- 👎 写作质量被描述为比 Opus 4.5 "更平淡" — 创意性散文减少，输出更机械化。过度自信行为：未经确认就执行破坏性操作。Pro 用户反映在高强度使用 2–3 小时后就会触及速率限制。2 月 10–11 日的 API 回退事件造成了大范围中断。

### Claude Sonnet 4.6

- 👍 "Sonnet 的价格，Opus 4.5 的能力" — Reddit 社区共识。在 Claude Code 内部测试中，70% 的用户更偏好 Sonnet 4.6 而非 Sonnet 4.5。OSWorld 得分 72.5% 是所有测试模型中最高的。
- 👎 复杂的多步骤任务仍然需要 Opus 级别的模型。部分开发者反映 4.6 系列的 token 消耗高于 4.5，一定程度上抵消了成本优势。

### Claude Opus 4.5

- 👍 首个在 SWE-bench Verified 上突破 80% 的模型。"它就是能理解" 架构模式和大规模重构 — Reddit r/ClaudeCode。Token 效率在前沿模型中最优。
- 👎 过度自主倾向：未经询问就重写整体架构，过度添加代码注释和文档。用户反映在接近思考 token 上限时出现"记忆焦虑"，导致输出仓促或被截断。

### Claude Sonnet 4.5

- 👍 Replit 报告切换后代码编辑错误率从 9% 降至 0%。"就像和一位资深工程师结对编程" — Skywork AI。在日常编码任务中实现了速度与质量的良好平衡。
- 👎 "自信地谎称已经阅读了文档" — Reddit r/cursor。长上下文检索能力弱：在 256K token 时准确率仅 18.5%。许多用户认为相比 Sonnet 4 "提升不大"，尤其是在非编码任务上。

### GPT-5.3 Codex

- 👍 "启动一个任务，离开几个小时，回来就是可运行的软件" — Matt Shumer。Terminal-Bench 第一名，77.3%。社区共识：用 Opus 做规划和架构设计，用 Codex 并行执行定义明确的任务。
- 👎 多位用户反映高峰期被静默路由到 GPT-5.2。Spark 模式："很少有逻辑错误，但会添加垃圾代码和不必要的抽象。" 有用户花了 100 美元的 Opus 额度专门清理 Codex 生成的仪表盘。

### Gemini 3 Pro

- 👍 最初被誉为"明显优于 GPT-5.2 和 Opus 4.5" — Reddit。GPQA Diamond 91.9% 是单模型最高分。脚手架搭建、重构和结构化输出受到企业用户好评。
- 👎 尽管有 1M 窗口，长上下文质量在 50K token 后明显下降。发布后速率限制大幅削减（RPM −67%，RPD −80%）。"API 在美国工作时间经常不可用。" 在小众或领域特定话题上的幻觉问题仍然令人担忧。

### Gemini 3 Flash

- 👍 "成为我默认选择的平价模型" — 热门博文标题。输出速度 218 tok/s，比 GPT-5.2 快 1.7 倍。SWE-bench 78.0% 超过 Gemini 3 Pro（76.2%），小模型在智能体编码上击败大模型的罕见案例。
- 👎 Vectara 基准测试幻觉率约 91%。免费配额从 250 RPD 削减至 20 RPD。"停不下来地输出代码注释" — 开发者反映过多的行内文档导致 token 用量膨胀。

### GLM-5

- 👍 Humanity's Last Exam 50.4% 超过 GPT-5.2 和 Opus 4.5。Vectara 基准测试幻觉率 34%，为行业最低。"比 GLM-4.7 好了不知道多少个量级" — Reddit。完全 MIT 开源，零 NVIDIA 依赖（可在昇腾 NPU 上运行）。
- 👎 推理速度慢，仅 17–19 tok/s。智能体模式编码在复杂多文件任务上仍落后于闭源模型。需要比 Claude 更精确和结构化的提示词才能获得最佳效果。

### Kimi K2.5

- 👍 视觉编码工作流广受好评 — 截图或录屏即可生成可运行代码。OCRBench 92.3% 为所有模型中最高。Agent Swarm 支持最多 100 个并发智能体。定价约为 Claude 的 1/40，适合大规模使用。
- 👎 "用它写了一周代码，结论：不行" — V2EX 用户评价。temperature=0 时输出一致性为 0%（确定性问题）。逻辑混乱：有用户的智能体意外地 git 回滚了整个代码库。交互式使用时推理速度偏慢。

### MiniMax M2.5

- 👍 SWE-bench Verified 80.2% — 非 Anthropic 模型中的 SOTA。"智能便宜到可以忽略不计" — 输出定价 $1.10/1M tokens。Lightning 模式 100 tok/s。MiniMax 称内部 30% 的公司任务现已由 M2.5 完成。
- 👎 幻觉基准测试得分 88%，位于第 36 百分位。复杂编码任务在多次运行间表现不一致。指令遵循率 65%（第 68 百分位），意味着偶尔会忽略约束条件或格式要求。

---

## 选型建议

| 使用场景 | 推荐模型 |
|---------|---------|
| 长上下文 + 深度推理 | Claude Opus 4.6（1M beta）、Gemini 3 Pro |
| 编码 + 智能体执行 | GPT-5.3 Codex、Claude Opus 4.6、MiniMax M2.5 |
| 高性价比编码 | Gemini 3 Flash、Sonnet 4.6、GLM-5、MiniMax M2.5 |
| 快速迭代 / 前端开发 | GPT-5.3 Codex Spark、Kimi K2.5（视觉编码） |
| 开源 / 自部署 | GLM-5、Kimi K2.5、MiniMax M2.5 |
| 文档 / OCR / 多模态 | Kimi K2.5、Gemini 3 系列 |

## 说明

- 定价和配额随时可能变动，请以官方文档为准。
- 基准测试分数因评估设置而异，包括 pass@k 设置、工具可用性和思考预算级别。
- 用户评价来源于 Reddit、Hacker News、知乎、V2EX 和掘金 — 均为主观个人体验，不一定具有普遍代表性。

---

<p align="center">
  <sub>Maintained by <b>Mingxu Zhang</b> & <b>Zheng Gong</b></sub>
</p>
