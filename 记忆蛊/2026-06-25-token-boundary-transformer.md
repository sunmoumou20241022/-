---
name: token-boundary-transformer-notes
description: 第一周第一日笔记完成：Token边界原理 + Transformer架构，结合A1论文
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

# Token 边界 + Transformer 笔记 — 2026-06-25

## 完成了什么

完成了学习计划**第一周第一日**的笔记：Token 边界原理 + Transformer 架构。

## 关键文件

- **第一日笔记**: `D:\网安\网安\一年之约\第一周\第一日.md`
- **A1 论文**: *Attention Is All You Need*（arxiv:1706.03762）
- **论文笔记**: `D:\网安\网安\论文\A1（Attention Is All You Need（Transformer 原始论文）.md`

## 核心知识

### Token 边界原理

- Token = LLM 看到的"最小单位"，不是人类看到的"字符"或"单词"
- Tokenizer 的切分方式和人类理解的"词边界"不一致
- 攻击者可以通过操纵 token 边界隐藏恶意内容：
  - 加空格：`"炸弹"` → `"炸" + "弹"`
  - Unicode 操纵：零宽字符插入
  - BPE 切分：低频词被拆成多个 token

**安全意义**：安全检测在"字符层"做，LLM 在"Token 层"理解 → 两层映射不一致 → 攻击窗口

### Transformer 架构（A1 论文）

| 组件 | 要点 |
|------|------|
| Encoder | 6 层，每层 2 个子层（Self-Attention + FFN） |
| Decoder | 6 层，每层 3 个子层（Masked Self-Attention + Cross-Attention + FFN） |
| Scaled Dot-Product Attention | $\text{softmax}(QK^T / \sqrt{d_k})V$ |
| Multi-Head Attention | h=8 个头，每头维度 64 |
| Positional Encoding | Sinusoidal，波长几何级数 |
| FFN | 两层 MLP，中间维度 2048 |

**训练**：Adam + warmup 4000 步 + learning rate decay

**结果**：EN→DE 28.4 BLEU，EN→FR 41.8 BLEU，3.5 天训练

### Token → Transformer 流程

```
原始文本 → Tokenizer → Token IDs → Embedding → Transformer
```

攻击层级：
1. Tokenizer 层：Token boundary manipulation
2. Embedding 层：Embedding poisoning
3. Transformer 层：Attention manipulation

## 下一步（第二日）

- Prompt Injection 原理分析
- 基于 Token 边界理解，深入分析注入攻击

## 相关记忆

- [[p1-skeleton-progress]] — P1 项目进度
- [[rlhf-alignment-tax-notes]] — RLHF 对齐税（第五日）