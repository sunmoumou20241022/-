---
name: claudemd-v25-upgrade
description: 底层蛊从v2.4升级到v2.5，新增QDF新鲜度分级、搜假设本身、引用质量五条；4/5/6工具规格写入Obsidian
metadata: 
  node_type: memory
  type: feedback
  confidence: high
  date: 2026-06-30
  originSessionId: 2f3e7c6b-4806-411a-a5a4-d38b820cf8c1
---

## 底层蛊 v2.4 → v2.5 迭代

**触发**：用户下载了 system_prompts_leaks-main.zip，问"这里面有没有优化搜索工具或者其他辅助的"

**深读文件**：
- `OpenAI/tool-file_search.md` → QDF 新鲜度分级
- `OpenAI/gpt-5.5-thinking.md` → 搜假设本身 + 引用质量五条
- `OpenAI/tool-advanced-memory.md` → 记忆分层四层结构
- `Anthropic/Claude Code/bundled-skills/deep-research/scripts/workflow-script.js` → 对抗式验证 workflow
- `Perplexity/perplexity-computer.md` → 搜索工具分工表
- `Anthropic/anthropic_reminders.md` → Claude 提醒机制（安全相关，未借鉴）
- `Anthropic/sonnet-4.6-reminders.md` → 安全分类器提醒（安全相关，未借鉴）

**1/2/3 写入文档（CLAUDE.md v2.5）**：
1. QDF 新鲜度分级 Q0-Q4 → 一、核心铁律，搜索决策树后新增
2. 时间不稳定假设要搜假设本身 → 一、核心铁律，禁止行为后新增
3. 引用质量五条 → 四、信息质量原则，规则6 扩充
4. 自检清单扩充 → A5/A6/D 三项新增

**4/5/6 写入工具使用（Obsidian 记忆蛊）**：
4. 对抗式验证 Workflow 3票制 + 完整 Schema → `D:\网安\网安\记忆蛊\2026-06-30-search-and-tool-specs.md`
5. 搜索工具分工表 + QDF 参数 + 硬性规则 → 同上
6. 记忆分层 Schema（四层结构 + origin 标注建议） → 同上

**Why**: v2.4 搜索决策只有"搜不搜"一维，缺少新鲜度事前预判和假设稳定性检查；引用只要求"有来源"不要求"来源可信"。
**How to apply**: 下次搜索前先判断 Q0-Q4 档位；检查是否有"默认为真"的时间不稳定假设；引用时检查多元性和权威占比。
