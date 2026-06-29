---
name: obsidian-graph-color-config
description: Obsidian Graph View颜色分组配置完成，4个文件夹已上色
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fe16164-812f-40c7-a517-6d9a14dde7ae
---

# Obsidian Graph View 颜色配置 — 2026-06-26

## 完成了什么

配置了 Obsidian 官方 Graph View 的颜色分组，按文件夹区分节点颜色。

## 当前配色

| 文件夹 | 颜色 |
|--------|------|
| 一年之约 | 绿色 |
| 华为知识 | 蓝色 |
| 论文 | 黄色 |
| windows | 青色 |

## 关键教训

- **不能直接改 `.obsidian/graph.json` 文件**，Obsidian 关闭图谱时会用内存状态覆盖文件
- 必须在 Obsidian 界面里操作：图谱左上角 ⋮ → Color groups → Add color group
- 规则格式：`path:文件夹名`（注意 Obsidian 会自动在末尾加空格，这是正常的）
- 颜色格式是 `{a:1, rgb:整数}` 不是 `{r,g,b}`

## 还没配的文件夹

- 基础（紫色）
- 记忆蛊（玫红）
- 步骤（橙色）
- 周日加餐（棕色）

## 相关操作

- 删除了 Juggl 插件（2023年停更，无中文，不好用）
- 删除了 Excalidraw 插件及画布文件
- 清空了 community-plugins.json
- Canvas 核心插件已启用但暂未使用

## 相关记忆

- [[notion-to-obsidian-migration]] — Notion迁移Obsidian
