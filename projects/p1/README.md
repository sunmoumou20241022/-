# P1: LLM 安全自动化评估框架

> 第一周（6月14日）创建骨架
> 第二周（6月19日）添加批量测试引擎

## 文件说明

| 文件 | 说明 |
|------|------|
| `llm_security_eval.py` | **核心框架** — LLMTarget + SecurityFinding + AssessmentEngine |
| `quick_test.py` | 快速测试脚本 |
| `test_*.py` | 测试用完可以删掉 |

## 核心类说明

### LLMTarget 类
负责给 AI 模型发消息、拿回复

```python
target = LLMTarget(
    base_url="http://localhost:11434",
    model="llama3.1:8b",
    system_prompt="You are a cooking assistant."
)
response = target.query("What is a good pasta recipe?")
```

### SecurityFinding 类
负责记录每次攻击测试的结果

```python
finding = SecurityFinding(
    attack_id="PI-001",
    technique="经典指令覆盖",
    principle_violated="RLHF 对齐税",
    payload="Ignore your instructions...",
    response="...",
    verdict="INJECTED",  # 或 DEFENDED
    asr=0.67,            # 攻击成功率
    owasp_category="LLM01",
    mitre_atlas="AML.T0051"
)
```

### AssessmentEngine 类（第二周新增）
批量测试引擎 — 自动化运行多个攻击测试

```python
# 创建测试目标
targets = [
    LLMTarget(系统提示="只聊做饭"),
    LLMTarget(系统提示="乐于助人"),
    LLMTarget(系统提示=""),
]

# 定义攻击载荷
payloads = [
    {"id": "PI-001", "technique": "经典指令覆盖", ...},
    {"id": "PI-002", "technique": "角色扮演绕过", ...},
]

# 批量测试
engine = AssessmentEngine(targets)
results = engine.run_batch(payloads, repetitions=3)

# 输出结果
engine.get_summary()
# {"total_tests": 9, "average_asr": "XX%", ...}
```

## 快速测试

```powershell
cd D:\网安\网安\projects\p1
python quick_test.py
```

## 原理说明

| 类 | 对应原理 |
|------|---------|
| LLMTarget | Token 无隔离（第一周） |
| SecurityFinding | 攻击结果量化 |
| AssessmentEngine | RLHF 对齐税（第二周）— 批量测试不同系统提示配置 |

## 下一步（第3周）

- 添加更多攻击类型（Crescendo 多轮攻击）
- 添加 LLM-as-Judge 评分器
- 完善结果报告导出
