---
name: claudemd-v252-guide-borrow
description: 底层蛊v2.5.2从Claude Code社区指南(longform/shortform)借鉴，新增firecrawl搜索替代+Hooks强制自检+跨会话持久化+失败路径登记+子任务验收+Skills固化
metadata:
  node_type: memory
  type: feedback
  confidence: high
  date: 2026-07-02
  originSessionId: current
---

## 底层蛊 v2.5.1 → v2.5.2 从社区指南借鉴

**触发**：用户给了两份 Claude Code 社区指南（Anthropic hackathon 冠军写的），问"有没有值得改的"+"WebSearch 用不了怎么办"

**深读文件**：
- `C:\Users\Administrator\Downloads\the-longform-guide.md` — token优化、记忆持久化hooks、验证模式、并行策略、subagent迭代检索
- `C:\Users\Administrator\Downloads\the-shortform-guide.md` — skills/commands、hooks、subagent、MCP上下文管理、firecrawl MCP配置

**6条改进写入 CLAUDE.md**：

1. 搜索工具优先级链 + firecrawl 替代 → 三、规则6修订（firecrawl_search为默认，WebSearch仅Anthropic API可用时）
2. 规则18 Hooks强制自检 → 八、新增（QDF提醒/时效性告警/搜索降级/改述拦截四个hook）
3. 6.6 跨会话持久化 → 六、新增（.tmp三字段 + PreCompact/Stop/SessionStart三hooks）
4. 规则12.1 失败路径登记 → 七、新增（计划时列已排除方案及理由）
5. 15.1 子任务验收原则 → 十五、新增（评估→追问→回取，max 3轮，传objective context）
6. 15.2 Skills固化高频工作流 → 十五、新增（4个候选skill）

**firecrawl MCP 配置**：
- 文件：`C:\Users\Administrator\.claude\.mcp.json`
- 模式：keyless远程（https://mcp.firecrawl.dev/v2/mcp），免费1000页/月
- 需重启 Claude Code 生效

**WebSearch 不可用根因**（已验证）：
- WebSearch是Anthropic server-side tool，硬绑定api.anthropic.com
- 第三方API（GLM-5.2）不实现Anthropic服务端搜索基础设施
- 这是硬性架构限制，无官方workaround
- 证据来源：docs.claude.com server-tools页（2026-07-02 WebFetch抓取）

**未深查的方案**：Chrome in Claude / context7 / tavily-mcp / brave-search-mcp / exa-mcp（第6个agent未跑完）

**Why**: v2.5.1搜索工具表还指向WebSearch但实际不可用；自检靠自觉无兜底；跨会话无结构化接续；子任务返回无验收；高频工作流每次重解析易漏步骤；只记教训不记死路。
**How to apply**: 下次搜索时用firecrawl_search（重启后生效）；长对话过载时按6.6存.tmp；给计划时列"已排除方案"；子任务返回值先验收再采纳。关联 [[claudemd-v251-context-rewrite]] [[claudemd-v25-upgrade]]。
