---
name: claudemd-v251-context-rewrite
description: 底层蛊第六节上下文管理重写，新增压缩存档9段协议+防漂移自检+无缝继续理念
metadata:
  node_type: memory
  type: feedback
  confidence: high
  date: 2026-07-01
  originSessionId: 2f3e7c6b-4806-411a-a5a4-d38b820cf8c1
---

## 底层蛊 v2.5 → v2.5.1 第六节重写

**触发**：上一对话压缩存档后，用户说"继续重写第六节"（待办遗留）

**深读文件**：
- `Anthropic/Claude Code/bundled-skills/compact.md` → 9段摘要模板（Primary Request/Key Concepts/Files/Errors/Problem Solving/All user messages/Pending/Current Work/Next Step）
- `Anthropic/Claude Code/claude-code-opus-4.8.md` → 摘要后无缝继续，不提前收尾
- `Anthropic/anthropic_reminders.md` → long_conversation_reminder 防漂移（旁观者/起点/累积检验）

**写入 CLAUDE.md 第六节（5个子节）**：
1. 6.1 自检节奏锚点（保留轮数分档，31+从"另开对话"改为"压缩存档后继续"）
2. 6.2 防漂移自检（旁观者/起点/累积三检验，借鉴 long_conversation_reminder）
3. 6.3 压缩存档9段协议（固定顺序，第6段逐字保留用户消息，第9段带原话引用）
4. 6.4 摘要三条铁律（用户消息逐字保/Next Step带原话/长独白单独压）
5. 6.5 摘要后无缝继续（禁止重复铺陈、禁止提前收尾、摘要是接力棒）

**同步更新**：
- frontmatter version 2.4 → 2.5（标题已是v2.5，frontmatter漏改，本次补上）
- 第九节新增【迭代#6】v2.5.1 记录

**Why**: 原第六节只有轮数分档表，三个缺口——(1) 31+要求"另开对话"与Claude Code实际做法冲突；(2) 无压缩存档结构化模板，摘要质量参差；(3) 只防失忆不防漂移。
**How to apply**: 下次长对话过载时，按9段协议生成摘要（尤其第6段逐字保用户消息、第9段带原话）；摘要后贴回继续，不重复铺陈。关联 [[claudemd-v25-upgrade]]。
