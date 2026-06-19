---
name: rlhf-alignment-tax-notes
description: 第二周周一完成RLHF对齐税原理笔记，写到第五天.md
metadata: 
  node_type: memory
  type: project
  originSessionId: dd7df5a5-065f-4b9b-8f6e-8f1895ab9803
---

# 2026-06-15 学习记录

## 今天做了什么

完成了学习计划**第二周周一（理解日）**的任务：理解 RLHF 三阶段，写"对齐税"笔记。

## 关键文件

- **第五天笔记**: `D:\网安\网安\一年之约\第五天.md`（RLHF对齐税原理）
- **学习计划**: `D:\网安\网安\一年之约\一年之约.md`
- **P1项目**: `D:\网安\网安\projects\p1\llm_security_eval.py`（周四已创建骨架）

## 学到的核心知识

### RLHF 三阶段
1. **SFT**（监督微调）— 用人类示范数据训练，约1.3万条
2. **RM**（奖励模型）— 训练AI裁判，约3.3万条排名数据
3. **PPO**（强化学习）— 模型刷分优化

### 对齐税（Alignment Tax）
- 定义：追求安全对齐的代价，模型在某些任务上性能下降
- 原因：目标冲突（服从 vs 安全）、过度谨慎、分布偏移
- 证据：InstructGPT在SQuAD、DROP等公开数据集上性能下降
- 解决办法：混入预训练数据（PPO-ptx）

### 与提示注入的关系
- RLHF训练"服从用户"，但与"遵守系统提示"存在张力
- 越狱利用了RLHF的"服从"倾向
- none配置（无系统提示）时攻击成功率最高

## 论文阅读

今天读了两篇论文：
- **A2**: InstructGPT (arXiv:2203.02155) — OpenAI的RLHF方法
- **A3**: Constitutional AI (arXiv:2212.08073) — Anthropic用AI反馈替代人类标注

两篇的关系：第二篇继承并改进了第一篇，用AI自我监督替代大量人工标注。

## 技术问题记录

- PowerShell 在工具调用中有时被安全classifier拦截，需要用Read+Edit替代Write创建新文件
- Ollama OpenAI兼容接口（/v1/chat/completes）在当前环境下超时

## 下一步（周二）

- 实验日：三种系统提示配置对比攻击成功率
- 代码在 `projects/p1/` 目录下
