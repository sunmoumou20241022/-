---
name: claudemd-v300-modular-reform
description: 底层蛊v3.0模块化大改革：单CLAUDE.md(1093行)拆为宪法+索引(280行)+11个rules+4个skills+2个agents+hooks
metadata:
  node_type: memory
  type: feedback
  confidence: high
  date: 2026-07-02
  originSessionId: current
---

## 底层蛊 v2.5.2 → v3.0 模块化大改革

**触发**：用户读了Claude Code社区指南(shortform+longform)后说"按他们的结构进行大改革"

**改革内容**：
1. **CLAUDE.md精简**：从1093行→约280行，只保留核心铁律+宪法级优先+态度原则+迭代记录+模块索引
2. **11个rules/文件**：search/citation-quality/self-check/context-management/efficiency/tool-safety/memory/copyright/boundaries/output-decisions/tool-orchestration
3. **4个skills/工作流**：/log-error /compact-archive /search-decide /paraphrase-check
4. **2个agents/子代理**：search-agent(搜索执行) + verify-agent(事实验证)
5. **Hooks落地**：QDF提醒(PreToolUse on搜索工具) + 会话存档(Stop)

**文件位置**：
- CLAUDE.md: C:\Users\Administrator\CLAUDE.md（宪法+索引）
- rules/: C:\Users\Administrator\.claude\rules\*.md（11个）
- skills/: C:\Users\Administrator\.claude\skills\*\SKILL.md（4个新建+2个已有）
- agents/: C:\Users\Administrator\.claude\agents\*.md（2个）
- hooks: C:\Users\Administrator\.claude\settings.json（hooks字段）
- 备份: C:\Users\Administrator\.claude\backups\CLAUDE-v2.5.2-backup.md

**每个rules/文件顶部声明**："上级规则：见 CLAUDE.md 核心铁律，冲突时以核心铁律为准"

**Why**: 单文件全量加载浪费token、模型定位规则难、高频工作流每次重新解析易漏步骤。模块化后rules/自动加载、skills按需触发、agents有限作用域。
**How to apply**: 下次会话自动加载rules/文件。需要错误日志时输/log-error。需要压缩存档时输/compact-archive。搜索前输/search-decide走决策树。引用前输/paraphrase-check改述自检。新规则写进对应rules/文件，不再改CLAUDE.md（除非是宪法级改动）。关联 [[claudemd-v252-guide-borrow]] [[claudemd-v251-context-rewrite]] [[claudemd-v25-upgrade]]。
