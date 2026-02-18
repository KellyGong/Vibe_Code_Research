# GLM-5 智谱AI 旗舰大模型调研报告

> 发布日期：2026年2月11日  
> 开发者：智谱AI（Z.ai），清华大学孵化，2026年1月完成香港IPO（募资约43.5亿港元）  
> 许可证：MIT（开源，支持商用部署与微调）  
> 数据截止：2026年2月18日

---

## 1. 模型规格

| 参数 | 数值 |
|------|------|
| 总参数量 | ~744B（7450亿） |
| 激活参数量 | ~44B（440亿） |
| 架构 | Mixture of Experts (MoE) |
| Expert 数量 | 256个，每token激活8个（稀疏率5.9%） |
| 预训练数据 | 28.5T tokens |
| 上下文窗口 | 200K tokens |
| 最大输出 | 128K tokens（131K） |
| 注意力机制 | DeepSeek Sparse Attention (DSA) + Multi-head Latent Attention (MLA) |
| 训练硬件 | 100,000块华为昇腾910B芯片（MindSpore框架，零NVIDIA依赖） |
| 推理速度 | ~17-19 tokens/sec |
| 幻觉率 | 34%（行业最低，前代GLM-4.7为90%） |

### 与前代对比

| 规格 | GLM-5 | GLM-4.5 |
|------|-------|---------|
| 总参数 | 744B | 355B |
| 激活参数 | 44B | 32B |
| Expert数 | 256 | 128 |
| 训练数据 | 28.5T | 15T |
| 上下文 | 200K | 128K |
| 最大输出 | 131K | 32K |

### 关键技术创新

- **Slime RL框架**：异步强化学习训练，打破传统顺序生成→评估→更新的瓶颈，引入Active Partial Rollouts (APRIL)，将幻觉率从90%降至34%（已开源：[THUDM/slime](https://github.com/THUDM/slime)）
- **DeepSeek Sparse Attention (DSA)**：高效长上下文处理，无需传统稠密注意力的算力开销
- **Multi-head Latent Attention (MLA)**：相比标准多头注意力减少33%内存开销
- **全国产芯片训练**：完全基于华为昇腾910B + MindSpore，无需美国半导体硬件

---

## 2. 定价

### API 定价

| 项目 | 价格 |
|------|------|
| 输入 | $1.00 / 百万tokens |
| 输出 | $3.20 / 百万tokens |

### 与竞品价格对比

| 模型 | 输入 ($/M tokens) | 输出 ($/M tokens) | 许可证 |
|------|-------------------|-------------------|--------|
| **GLM-5** | **$1.00** | **$3.20** | **MIT（开源）** |
| GPT-5.2 | $6.00 | $30.00 | 闭源 |
| Claude Opus 4.6 | $5.00 | $25.00 | 闭源 |
| Gemini 3 Pro | $2.00 | $12.00 | 闭源 |
| Kimi K2.5 | $0.60 | $2.50 | Modified MIT |

GLM-5 比 GPT-5.2 便宜约 **6倍（输入）/ 9倍（输出）**，是唯一前沿级MIT开源模型。

### 历史定价（GLM-4系列参考）

- GLM-4-Plus：降价90%后为 **5元/百万tokens**（约$0.69/M）
- GLM-4-Long（1M上下文）：**0.001元/千tokens**（即1元/百万tokens）

### 2026年2月价格调整

- 国内市场：订阅价格上涨至少30%，取消首购优惠
- 海外市场：API调用价格上涨67-100%，订阅价格上涨30-60%
- 老用户享有缓冲期，原价不变

### 免费使用

- [chat.z.ai](https://chat.z.ai/) 提供免费聊天，无需注册
- NVIDIA NIM 免费层可用
- 开源权重可从 HuggingFace / ModelScope 下载自部署

---

## 3. Benchmark 性能

### 主要基准测试成绩

| Benchmark | GLM-5 | GPT-5.2 | Claude Opus 4.6 | 说明 |
|-----------|-------|---------|-----------------|------|
| SWE-bench Verified | **77.8%** | 76.2% | 80.8% | 真实软件工程任务 |
| Humanity's Last Exam | **50.4%** | 47.8% | 46.2%* | *Opus 4.5分数 |
| BrowseComp | **75.9** | 72.1 | 68.4 | 网页浏览与研究 |
| Terminal-Bench 2.0 | 56.2% | 64.7% | 65.4% | 命令行Agent编程 |
| GPQA-Diamond | 68.2%~86.0% | 71.5% | 69.8% | 研究生级科学问答 |
| AIME 2025 | 88.7% | 100% | 92.3% | 高级数学竞赛 |
| AIME 2026 I | 92.7% | — | — | 最新数学竞赛 |
| AA Omniscience Index | **-1** | 34 | 28 | 幻觉指标（越低越好） |
| MCP-Atlas | **67.8** | — | ~67 | Agent工具调用 |

### GLM-5 的优势领域

- **性价比**：达到闭源模型~95%性能，成本仅~15%
- **Humanity's Last Exam**：50.4%，超越GPT-5.2和Claude Opus 4.5
- **知识检索**：BrowseComp 75.9，开源模型第一
- **幻觉抑制**：AA Omniscience Index -1，行业最佳
- **LMArena Text Arena**：开源模型排名第一

### GLM-5 的不足

- **长上下文**：200K vs Opus 4.6的1M token（beta）
- **推理速度**：17-19 tok/s vs 竞品25-30+ tok/s
- **数学**：AIME 88.7% vs GPT-5.2的100%
- **Agent编程**：Terminal-Bench 56.2% vs Opus 65.4%（差距9个百分点）

---

## 4. 开发者评测与社区反馈

### 正面评价

**编程能力（掘金、Reddit）：**
- 多位开发者认为GLM-5工程能力已与Claude Opus 4.5同一梯队
- Laravel转Next.js：自动安装依赖、编译脚本，一次性生成准确代码，体验优于Claude Opus
- 后端代码可靠性好，报错少；错误调试分析清晰、方案多元
- 前端设计、3D动画、网页游戏生成表现出色
- Reddit用户称"比GLM-4.7好了几个数量级"（lightyears better）
- 自调试能力强：能读取日志并迭代修复错误，而非简单重新生成

**Agent能力：**
- 支持数小时多阶段任务自动化运行，保持上下文连贯
- 具备自我反思与纠错机制
- 复杂系统处理、后端任务、系统重构、深度调试表现优秀

### 负面评价

**响应速度：**
- 平均响应时间130秒（GLM-4.7为96秒，增加35%）
- 推理速度17-19 tok/s，明显慢于NVIDIA硬件上的竞品

**中文能力：**
- 中文综合评测准确率71.0%
- 部分指标如Agent调用能力反而下滑（相比前代）

**编程局限（Reddit）：**
- 部分场景仍落后于Claude Sonnet 4.5和Opus，后者能立即解决的问题GLM-5可能卡住
- 替代Opus用于Claude Code时，代码质量有明显下降
- 需要更精确的prompt，对上下文的隐式理解不如Claude

**成本变化：**
- 每千次调用费用从52.5元上升至61.2元（增幅16.6%），但token消耗优化了9%

### 开发者共识

> GLM-5是国产编程模型的重要里程碑。在特定工程任务上可媲美Opus 4.5，是开源阵营的SOTA选择。但在Agent编程和推理速度上仍有差距，适合作为高性价比的主力模型，复杂任务可搭配闭源模型使用。

---

## 5. 接入方式

### API 接入（OpenAI兼容）

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-z-ai-api-key",
    base_url="https://api.z.ai/api/paas/v4/"
)

response = client.chat.completions.create(
    model="glm-5",
    messages=[
        {"role": "system", "content": "You are a senior software engineer."},
        {"role": "user", "content": "Review this code for security vulnerabilities."}
    ],
    temperature=0.7,
    max_tokens=4096
)
```

### OpenRouter 接入

```python
client = OpenAI(
    api_key="your-openrouter-key",
    base_url="https://openrouter.ai/api/v1"
)
response = client.chat.completions.create(
    model="z-ai/glm-5",
    messages=[{"role": "user", "content": "..."}]
)
```

### Reasoning Mode（推理模式）

```python
response = client.chat.completions.create(
    model="glm-5",
    messages=[{"role": "user", "content": "证明素数有无穷多个"}],
    extra_body={"reasoning": True}
)
```

### 自部署（vLLM）

```bash
# HuggingFace: zai-org/GLM-5 (MIT License)
# 硬件需求：~8× A100 80GB 或等效GPU
python -m vllm.entrypoints.openai.api_server \
    --model zai-org/GLM-5 \
    --tensor-parallel-size 8 \
    --max-model-len 200000 \
    --port 8000
```

### 访问渠道

| 渠道 | 链接 |
|------|------|
| 免费聊天 | [chat.z.ai](https://chat.z.ai/) |
| API平台 | [docs.z.ai](https://docs.z.ai/) |
| HuggingFace | [zai-org/GLM-5](https://huggingface.co/zai-org/GLM-5) |
| ModelScope | [THUDM](https://modelscope.cn/organization/THUDM) |
| OpenRouter | [z-ai/glm-5](https://openrouter.ai/z-ai/glm-5) |
| GitHub | [zai-org/GLM-5](https://github.com/zai-org/GLM-5) |
| NVIDIA NIM | 免费层可用 |

---

## 6. GLM系列发展时间线

| 时间 | 事件 |
|------|------|
| 2024年6月 | GLM-4 发布，对标GPT-4 |
| 2025年4月 | GLM-4-32B-0414系列开源（含推理模型GLM-Z1，速度200 tok/s） |
| 2025年4月 | GLM-4-Plus 降价90%至5元/百万tokens |
| 2025年8月 | GLM-4.5系列开源（355B MoE，含视觉模型GLM-4.5V） |
| 2025年9月 | GLM-4.6 发布（357B，200K上下文） |
| 2026年1月 | 智谱AI香港IPO，募资43.5亿港元 |
| 2026年1月 | GLM-5训练接近完成，内部测试启动 |
| 2026年2月11日 | **GLM-5正式发布** |
| 2026年Q1（预计） | GLM-5 MIT开放权重版本发布 |

---

## 7. 总结

GLM-5是目前最强的开源大语言模型之一，744B MoE架构在多项基准上接近甚至超越GPT-5.2和Claude Opus 4.6，同时价格仅为闭源竞品的15-20%。全程基于华为昇腾芯片训练，MIT许可开源，标志着国产AI基础设施的重要里程碑。

核心竞争力在于：极低幻觉率（行业最佳）、强工程编程能力、200K长上下文、以及极具竞争力的定价。主要短板是推理速度较慢（17-19 tok/s）、Agent编程能力与顶级闭源模型仍有差距、以及生态成熟度不足。

适用场景：高性价比AI后端、事实准确性要求高的内容生成、开源合规要求、自部署需求。建议搭配闭源模型处理复杂Agent编程和数学推理任务。
