---
name: notion-to-obsidian-migration
description: Notion 笔记批量迁移到 Obsidian Vault，含清洗脚本和使用流程
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

# Notion → Obsidian 迁移 — 2026-06-19

## 今天做了什么

完成了 Notion 笔记批量迁移到 Obsidian Vault，共导入 **23 篇笔记 + 10 张图片 + 3 个 docx**。

## 迁移的笔记

### 第一批：基础（8 篇 + 10 张图 + 1 docx）
- 云端渗透跳板机搭建指南、什么是URL、kali更新补全键、burp各种的意义
- Ollama 底层架构与部署逻辑、PDF格式翻译、进制转化 docx、页面PDF格式翻译和自动排版记笔记

### 第二批：Windows Server（7 篇 + 1 docx）
- windows Server 2019 创建域、DNS、ftp、CA 申请证书与 HTTP 重定向 HTTPS
- 第一次考试总结 + Windows第一次考核试题、组策略

### 第三批：华为网络（6 篇 + 1 docx）
- 二进制、配置IP地址、VLAN 跨交换机通信、跨交换机非对称安全隔离（魔术链路）
- eNSP 网络设备 AAA 认证实、第一次测试

## 关键工具

### 清洗脚本

- **位置**: `C:\Users\Administrator\notion_to_obsidian.py`
- **用法**:
  ```powershell
  python notion_to_obsidian.py "<解压后的Notion导出文件夹>" "<输出文件夹>"
  ```

### 自动处理的内容

| 问题 | 处理方式 |
|------|----------|
| 文件名带 UUID 后缀 | 自动去掉（如 `基础 33d92f88...md` → `基础.md`） |
| Notion 内部链接 `[标题](uuid.md)` | → Obsidian 双链 `[[标题]]` |
| 图片路径 URL 编码 | 解码为中文（`kali%E6%9B%B4...` → `kali更新...`） |
| 图片 alt 带 `.json` 后缀 | 去掉 |
| 多余空行 | 压缩 |
| 图片/附件 | 直接复制 |

## Notion 导出注意事项

1. 导出格式选 **Markdown & CSV**
2. 必须勾选 ✅ **Include sub-pages**（否则子页面不会导出）
3. 勾选 ✅ **Create folders for subpages**
4. 勾选 ✅ **Include attached files**
5. 下载的是 **双层 ZIP**（外层包装 + 内层 ExportBlock-xxx.zip），需要解压两次
6. 第一次导出忘勾子页面，只有索引页没有内容，需要重新导出

## Vault 最终结构

```
D:\网安\网安\
├── 基础.md + 基础/          ← Notion 导入
├── windows.md + windows/     ← Notion 导入
├── 华为知识.md + 华为知识/    ← Notion 导入
├── 从Notion导入/             ← 清洗脚本中间输出（可删）
├── 一年之约/                 ← 原有学习计划
├── 论文/                     ← 论文笔记
└── projects/p1/              ← P1 项目代码
```

## Git 同步

- 三批笔记分两次提交并推送到 GitHub
- 提交记录：`从 Notion 导入基础笔记` + `从 Notion 导入 Windows Server 和华为网络笔记`

## 遗留问题

- **从Notion导入/** 文件夹还在 Vault 里，是清洗脚本的中间输出，确认不需要后可删除
- **CSV/数据库** 类型的 Notion 页面无法自动转为 Markdown 表格，需手动整理
- **docx 附件** 只是被复制过来，Obsidian 不能直接预览，可考虑后续转为 PDF

## 相关记忆

- [[week2-thursday-peft-progress]] — 同一天早些时候的 PEFT 学习进度
- [[p1-skeleton-progress]] — P1 项目骨架，Obsidian Vault 位置记录
