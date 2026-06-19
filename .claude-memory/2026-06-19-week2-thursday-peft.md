---
name: week2-thursday-peft-progress
description: 第二周周四完成 AssessmentEngine 批量测试引擎 + PEFT 微调攻击面
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

# 第二周周四进度 — 2026-06-19

## 今天完成了什么

完成了学习计划**第二周周四（编码日）**的任务：
1. P1 添加 AssessmentEngine 批量测试引擎
2. 周四加餐：PEFT 微调攻击面（恶意 LoRA adapter）

## 关键文件

- **周四笔记**: `D:\网安\网安\一年之约\第二周\第一日.md`
- **P1 代码**: `D:\网安\网安\projects\p1\llm_security_eval.py`
- **P1 README**: `D:\网安\网安\projects\p1\README.md`（已更新）
- **快速测试**: `D:\网安\网安\projects\p1\quick_test.py`

## P1 项目新增内容

### AssessmentEngine 类

| 方法 | 功能 |
|------|------|
| `run_batch(payloads, repetitions)` | 批量运行攻击测试 |
| `_judge(constraint, response)` | 判断攻击是否成功 |
| `get_summary()` | 获取测试结果摘要 |

### 测试验证

```
测试结果：
  ASR: 33%
  verdict: DEFENDED
  （模型大部分时候能守住）
```

## 学到的核心知识

### AssessmentEngine 的作用

> 把"手动测试"变成"自动化批量测试"

- 定义好目标和攻击
- 一键运行
- 自动判断结果
- 自动计算 ASR

### PEFT 微调攻击面（Qi et al. 2024）

**核心发现**：
- 安全对齐是"浅层"的 → 只在前几个 token
- LoRA 微调能低成本撕掉安全对齐
- 恶意 LoRA adapter 是新的供应链攻击载体

**LoRA 原理**：
```
原模型不动（冻结）
只加两个小矩阵 A、B
只训练这 6 万参数（原模型的 0.001%）
成本：几美元、几小时
```

**攻击流程**：
```
攻击者收集 300 条"有害问答对"
→ LoRA 训练"去安全" adapter
→ 上传到 HuggingFace
→ 用户下载加载
→ 模型行为改变（不安全了）
```

## 笔记命名规则（已记住）

> **格式：第几周\第几日.md**
> 
> 不再用"第几天.md"

## 下一步（周五）

- 用 RLHF 原理解释 Exp001 中的 PARTIAL 案例
- 在 `notes/principles/rlhf-alignment-tax.md` 补充 DPO/PEFT 内容

## Obsidian Vault 位置

- Vault 路径：`D:\网安\网安`
- 笔记目录：`D:\网安\网安\一年之约\`
- 项目目录：`D:\网安\网安\projects\p1\`

---

## Git 同步设置（2026-06-19 新增）

### 已完成

✅ Git 仓库初始化
✅ 提交所有笔记到本地仓库
✅ 推送到 GitHub 私有仓库

### GitHub 仓库信息

- **仓库地址**：https://github.com/sunmoumou20241022/-
- **类型**：私有仓库（只有自己能看）
- **Token**：已保存在本地 Git 配置中

### 以后同步笔记的步骤

```powershell
cd D:\网安\网安
git add .
git commit -m "更新笔记"
git push
```

### 换电脑恢复笔记

```powershell
# 新电脑上运行
git clone https://github.com/sunmoumou20241022/-.git

# 然后用 Obsidian 打开这个文件夹
```

### Git 设置步骤（备忘）

```
1. git init                                    # 初始化仓库
2. 创建 .gitignore                             # 忽略 .obsidian/ 等文件
3. git add .                                   # 添加所有文件
4. git commit -m "初始提交"                     # 提交
5. git branch -M main                          # 重命名分支
6. git remote add origin <仓库地址>            # 连接远程仓库
7. git pull --allow-unrelated-histories        # 拉取远程内容（如有）
8. git push -u origin main                     # 推送
```

### 安全提示

- Token 已保存在 Git 配置中，推送时自动使用
- 如 Token 泄露，去 GitHub → Settings → Tokens 删除重建