# Introduction 结构检查模块

## 检查目标

确保 Introduction 逻辑清晰，gap 与方法对应，contribution 明确。

## 标准 Introduction 结构

### 第1段：背景与重要性

**应包含**：
- 研究领域介绍
- 问题的重要性/应用价值
- 为什么这个问题值得研究

**检查点**：
- [ ] 是否清晰定义了研究问题
- [ ] 是否说明了问题的重要性

### 第2-3段：现有方法与局限性（Gap）

**应包含**：
- 现有方法的分类或发展脉络
- 每类方法的核心思想
- 每类方法的局限性（gap/challenge）

**检查点**：
- [ ] gap 是否具体明确（不是泛泛而谈）
- [ ] gap 是否有依据（引用或分析支撑）
- [ ] 多个 gap 之间是否有逻辑关系

### 第4段+：提出的方法

**应包含**：
- 方法的核心思想
- 如何解决前面提出的 gap
- 方法的主要特点/优势

**检查点**：
- [ ] 每个 gap 是否都有对应的解决方案
- [ ] 解决方案是否直接针对 gap（不是间接或部分解决）

### 最后1-2段：Contribution

**标准格式**：
```
Our contributions can be summarized as follows:
• We propose ... (方法贡献)
• We conduct ... (实验贡献)  
• We release ... (资源贡献，如有)
```

**检查点**：
- [ ] contribution 是否清晰列出（通常3-4点）
- [ ] 每点 contribution 是否具体（不是 "we propose a novel method"）
- [ ] contribution 是否与 gap 对应

## Gap-Solution 对应检查

这是最重要的检查项。

**方法**：
1. 提取所有明确提出的 gap/challenge
2. 提取所有 claimed solutions
3. 建立对应关系
4. 检查是否有：
   - 悬空的 gap（提出了但没解决）
   - 无源的 solution（解决方案没有对应的 gap）

**输出格式**：
```markdown
| Gap/Challenge | 位置 | 对应 Solution | 位置 | 对应强度 |
|---------------|------|--------------|------|----------|
| G1: 现有方法忽略X | L45-48 | S1: 我们引入模块A处理X | L89 | ✅ 强对应 |
| G2: 计算复杂度高 | L52 | - | - | ❌ 未解决 |
| - | - | S2: 我们使用技术B | L95 | ⚠️ 无对应gap |
```

## 常见问题模式

| 问题 | 描述 | 严重程度 |
|------|------|----------|
| Gap悬空 | 提出了问题但方法中没有解决 | 🔴 Critical |
| Solution无源 | 声称做了某事但没说明为什么需要 | 🟡 Major |
| 对应薄弱 | Gap和solution有关但不直接对应 | 🟡 Major |
| Contribution空泛 | "we propose a novel method" 无具体说明 | 🟢 Minor |
| 缺少importance | 没说明为什么这个问题重要 | 🟢 Minor |

## 输出模板

```markdown
## Introduction 结构检查结果

**状态**: [✅ 通过 / ⚠️ 发现问题]

### 结构完整性
| 部分 | 存在 | 质量 | 问题 |
|------|------|------|------|
| 背景与重要性 | ✅/❌ | 高/中/低 | |
| 现有方法与Gap | ✅/❌ | 高/中/低 | |
| 提出的方法 | ✅/❌ | 高/中/低 | |
| Contribution列表 | ✅/❌ | 高/中/低 | |

### Gap-Solution 对应表
[见上述格式]

### Contribution 分析
| # | Contribution内容 | 具体程度 | 对应Gap |
|---|-----------------|---------|---------|

### 详细问题
[对每个问题的具体描述和修改建议]
```
