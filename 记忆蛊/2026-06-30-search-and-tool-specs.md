---
name: 搜索与辅助工具规格
version: 1.0
description: 从 system_prompts_leaks 仓库提炼的三个可参照工具使用模式：对抗式验证 workflow、搜索工具分工表、记忆分层 schema
metadata:
  node_type: memory
  type: reference
  origin: system_prompts_leaks-main (2026-06-26 snapshot)
  last_updated: 2026-06-30
  confidence: high
---

# 搜索与辅助工具规格

> 从泄露的系统提示词中提炼的工具层设计模式，可直接参照用于 agent 编写或工具配置。

---

## 工具1：对抗式验证 Workflow（3票制）

**来源**：`Anthropic/Claude Code/bundled-skills/deep-research/scripts/workflow-script.js`

**用途**：深度研究场景下，对搜索提取的每个可证伪 claim 做多角度对抗验证，防止单一来源幻觉。

**流程**：
```
Scope（分解5角度）
  → Search（5并行WebSearch，每角度一个）
    → Fetch（URL去重 + fetch top 15 + 提取可证伪 claim）
      → Verify（每 claim 3票对抗验证，2/3 反驳才杀掉）
        → Synthesize（语义去重 + 按置信度排序 + 引用源）
```

**关键参数**：
| 参数 | 值 | 说明 |
|------|-----|------|
| VOTES_PER_CLAIM | 3 | 每个 claim 投 3 票 |
| REFUTATIONS_REQUIRED | 2 | 3 票中 2 票反驳才杀掉 |
| MAX_FETCH | 15 | 最多 fetch 15 个 URL |
| MAX_VERIFY_CLAIMS | 25 | 最多验证 25 个 claim |

**Schema 定义（可直接复用）**：

```json
// Scope 输出
{
  "question": "string",
  "summary": "string",
  "angles": [
    { "label": "string", "query": "string", "rationale": "string" }
  ]
}

// Search 结果
{
  "results": [
    { "url": "string", "title": "string", "snippet": "string", "relevance": "high|medium|low" }
  ]
}

// Fetch 提取
{
  "sourceQuality": "primary|secondary|blog|forum|unreliable",
  "publishDate": "string",
  "claims": [
    { "claim": "string", "quote": "string", "importance": "central|supporting|tangential" }
  ]
}

// Verify 判决
{
  "refuted": "boolean",
  "evidence": "string",
  "confidence": "high|medium|low",
  "counterSource": "string"
}

// Report 输出
{
  "summary": "string",
  "findings": [
    { "claim": "string", "confidence": "high|medium|low", "sources": ["url"], "evidence": "string", "vote": "string" }
  ],
  "caveats": "string",
  "openQuestions": ["string"]
}
```

**何时用**：需要深度多源事实核查时（对比 5+ 实体、从一手源建数据表、行业深研、市场规模估算）。
**何时不用**：简单查证、单源确认、快速问答。

---

## 工具2：搜索工具分工表

**来源**：`Perplexity/perplexity-computer.md` + `OpenAI/tool-web-search.md` + `OpenAI/tool-file_search.md`

**用途**：不同搜索场景应该用什么工具，以及硬性禁止规则。

| 工具 | 适用场景 | 禁止场景 |
|------|---------|---------|
| **WebSearch** | 时效信息（新闻/价格/版本/CVE）、获取新领域专业知识 | 需要登录的站点、招聘职位搜索 |
| **WebFetch** | 读取特定 URL 内容、从已知页面提取信息 | URL 不确定时（先 search 再 fetch） |
| **file_search (msearch)** | 用户上传文件/内部知识库的语义+关键词混合检索 | 网页搜索（用 WebSearch） |
| **学术垂直搜索** | 论文/出版物/一手学术源 | 产品查询、人员查询 |
| **人员垂直搜索** | 按姓名/角色/公司/地点找人 | 公司信息、商业名录、产品查询、评价 |
| **browser_task** | 网页交互（点击/填表/登录操作） | 不需要交互的纯信息获取 |

**硬性规则**（从 Perplexity 提炼）：

1. **招聘/职位搜索必须用 browser 浏览招聘站**，禁止用 web search——搜索引擎结果是过期+幻觉的职位链接
2. **file_search 的 QDF 参数**：查询时带新鲜度限定
   - `--QDF=0`：5+ 年历史或不变事实
   - `--QDF=1`：一般不过时，boost 18 月
   - `--QDF=2`：变化慢，boost 6 月
   - `--QDF=3`：可能变化，boost 90 天
   - `--QDF=4`：变化快，boost 60 天
   - `--QDF=5`：最新，boost 30 天
3. **实体名必须用 + 运算符**：如 `+(John Doe)` 而非拆开成 `John Doe`
4. **非英语查询必须双语搜索**：原文语言 + 英文各搜一遍

---

## 工具3：记忆分层 Schema

**来源**：`OpenAI/tool-advanced-memory.md`（ChatGPT 高级记忆的真实结构）

**用途**：设计记忆系统时区分"用户主动提供"vs"系统自动推断"的记忆，后者需降低置信度。

**四层结构**：

| 层 | 名称 | 来源 | 置信度 | 使用规则 |
|----|------|------|--------|---------|
| 1 | **Response Preferences** | 用户主动表达 | high | 直接指导回复风格 |
| 2 | **Topic Highlights** | 对话历史自动提取 | high | 维持上下文连续性 |
| 3 | **User Insights** | 对话推断 | medium | 须标注"推断，未验证" |
| 4 | **Interaction Metadata** | 系统自动生成（消息长度、使用模式、设备信息等） | low | 明确标注"自动生成，可能不准" |

**对比当前底层蛊记忆分类**：

| 底层蛊当前 | 对应 ChatGPT 层级 | 差异 |
|-----------|------------------|------|
| user | 层1 + 层2 | 没区分"用户主动说"vs"我观察到的对话模式" |
| feedback | 层3 | 一致 |
| project | 层2 | 一致 |
| reference | 无对应 | 底层蛊独有 |

**建议改进**：
- 记忆写入时标注 `origin: explicit | inferred | auto_generated`
- `inferred` 和 `auto_generated` 置信度降一档
- `auto_generated` 类记忆（如"用户平均消息长度5217字"）使用时必须说"系统观察，可能不准"

---

*三个工具规格均提炼自 system_prompts_leaks 仓库 2026-06-26 快照。模式可信，具体参数可能随各厂商更新而变化。*
