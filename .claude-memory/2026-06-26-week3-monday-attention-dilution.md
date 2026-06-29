---
name: week3-monday-attention-dilution
description: 第三周第一日笔记完成：Attention稀释原理 + Crescendo/TAP多轮攻击入门
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

# 第三周第一日笔记 — 2026-06-26

## 完成了什么

完成了学习计划**第三周第一日**的笔记：Attention 稀释原理 + Crescendo/TAP 多轮攻击入门。

## 关键文件

- **第一日笔记**: `D:\网安\网安\一年之约\第三周\第一日.md`
- **B6 论文**: *Crescendo: Multi-Turn LLM Jailbreak Attack*（arxiv:2404.01833）
- **B8 论文**: *Tree of Attacks with Pruning*（arxiv:2312.02119）
- **Lost in the Middle**: arxiv:2307.03172

## 核心知识

### Attention 稀释原理

- Softmax 归一化导致：上下文变长 → 早期 token 权重被稀释
- "Lost in the Middle" 现象：中间位置信息关注度 < 开头/结尾
- U-shaped 曲线：模型检索准确率随位置呈 U 形分布

### Crescendo 多轮攻击

| 机制 | 说明 |
|------|------|
| Soft touch | 非对抗式、渐进式攻击 |
| 对话连贯性 | RLHF 让模型倾向保持上下文一致 |
| Attention 稀释 | 多轮后系统提示权重降低 |

**核心思路**：从合规话题开始 → 逐步渐进偏离 → 每轮"看起来合理" → 不触发即时拒绝

### TAP vs PAIR

| 维度 | PAIR | TAP |
|------|------|-----|
| 结构 | 线性迭代 | 树形搜索 |
| 局部最优 | 容易陷入 | 分支避免 |
| 查询效率 | 较高 | 剪枝降低 |
| 成功率 | 中等 | 80%+ |

### 2025 年演化

- **Tempest** = TAP 树形搜索 + Crescendo 多轮渐进
- **M2S** = 多轮压缩单轮，ASR 反升 17.5%

## 下一步（第二日）

- Crescendo 实验：验证 Attention 稀释的实际效果
- 测试短/长系统提示的转折点差异

## 相关记忆

- [[token-boundary-transformer-notes]] — 第一周第一日：Token 边界 + Transformer
- [[rlhf-alignment-tax-notes]] — 第二周：RLHF 对齐税
