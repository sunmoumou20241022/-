---
name: week2-tuesday-wednesday-progress
description: 第二周周二实验 + 周三深化日完成，DPO/RLAIF笔记写入第七日.md
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

# 第二周进度更新 — 2026-06-18

## 今天完成了什么

完成了学习计划**第二周周二（实验日）补充 + 周三（深化日）**的任务。

## 关键文件

- **第六天笔记**: `D:\网安\网安\一年之约\第六天.md`（系统提示实验结果分析）
- **第七日笔记**: `D:\网安\网安\一年之约\第七日.md`（DPO vs PPO vs RLAIF + 对齐训练演化）
- **第五天笔记**: `D:\网安\网安\一年之约\第五天.md`（RLHF三阶段，周一已完成）

## 学到的核心知识

### 周二实验关键发现（修正原假设）

实验结果：
| 配置 | ASR |
|------|-----|
| restricted | 33.33% |
| helpful | **100%**（最危险） |
| none | 0% |

**原假设**：none 配置 ASR 最高
**实际发现**：helpful 配置 ASR 最高

**原因**：系统提示如果和 RLHF 的"有用性"目标一致（"Always help"），会放大模型的"听话"倾向，反而降低安全边界。

### 周三核心知识

**越狱 vs 提示注入**：
- 越狱是目标（绕过安全）
- 提示注入是手段之一（覆盖指令）

**DPO vs PPO vs RLAIF**：
- DPO = 自我蒸馏，用偏好数据让学生学会"好答案长什么样"
- DPO 解决工程问题（更稳定），不是对齐税问题（张力依然存在）
- RLAIF = 用 AI 代替人类标注偏好，便宜但引入数据投毒风险

**最新趋势（2024-2025）**：
- GRPO（DeepSeek）：用相对比较，不需要偏好对
- RLVR：用可验证奖励（数学/代码）
- Self-Play：模型自己训练自己
- 趋势：去人类化、自动化、规模化

## 下一步（周四）

- P1 添加 AssessmentEngine 批量测试引擎
- 周四加餐：PEFT 微调攻击面（恶意 LoRA adapter）

## Obsidian Vault 位置

- Vault 路径：`D:\网安\网安`
- 笔记目录：`D:\网安\网安\一年之约\`