---
name: monthly-update-2026-06
description: 2026年6月学习计划持续更新检查记录（首次建立机制）
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c8cbf8c-1abf-4a5d-b724-59802ed1a273
---

# 持续更新检查 — 2026-06

## 检查日期：2026-06-27

## 检查结果

| 类别 | 状态 | 变化详情 |
|------|------|---------|
| 论文 | 已核实 | G2-G6编号均正确确认 |
| 工具 | 有更新 | PyRIT v0.9→v0.14，仓库迁移 Azure→microsoft |
| 价格 | 有变化 | CASP $1099→$899，DeepSeek定价结构更新 |
| OWASP | 无更新 | ASI01-10仍为最新 |

## 已修正的文档位置

- 第291行：PyRIT版本 v0.9+ → v0.14+
- 第894行：PyRIT链接 Azure → microsoft
- 第1664行：CASP价格 $1099 → $899
- 第269行：G5论文编号 "未核实" → 2404.02151
- 第1673行：DeepSeek价格说明更新为cache hit/miss结构
- 新增"持续更新机制"章节（第170行后插入）

## 核实确认的论文编号

全部正确，无需修正：
- B6 Crescendo: 2404.01833 (USENIX Security 2025)
- B8 TAP: 2312.02119 (NeurIPS 2024)
- E10 Refusal Direction: 2406.11717
- E11 Harmfulness/Refusal Separation: 2507.11878
- G2 AutoDAN-Turbo: 2410.05295 (ICLR 2025 Spotlight)
- G3 Tempest: 2503.10619 (ACL 2025 Main)
- G6 Jailbreak-Tuning: 2507.11630

## 重要发现：PyRIT仓库已迁移

- **旧地址**：https://github.com/Azure/PyRIT（已归档，只读）
- **新地址**：https://github.com/microsoft/PyRIT
- **最新版本**：v0.14.0（2025-06-05）

## 重要发现：DeepSeek API变化

- **定价结构**：改为 cache hit / cache miss 双层定价
- **模型名更新**：`deepseek-chat` 和 `deepseek-reasoner` 已于 2026年7月弃用
- **新模型名**：`deepseek-v4-flash`（性价比高）、`deepseek-v4-pro`

## 下月重点关注

- [ ] 搜索2026年6-7月新发表的LLM安全论文
- [ ] 关注OWASP GenAI是否有ASI更新
- [ ] 核实CISP考试价格是否有变化

## 相关记忆

- [[week3-monday-attention-dilution]] — 第三周笔记（TAP/Crescendo）
