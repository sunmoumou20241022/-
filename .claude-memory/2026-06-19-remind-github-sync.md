---
name: remind-github-sync
description: 每次完成任务后提醒用户将笔记和记忆同步到 GitHub
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 532c7a28-73a9-40a8-9db6-791e91dfcfd8
---

# 完成任务后提醒 GitHub 同步

**Why:** 用户要求每次完成任务后提醒同步，避免笔记和记忆丢失，确保换电脑时能恢复。

**How to apply:** 每次完成一个任务后，在回复结尾加上提醒：

> 💾 提醒：记得同步笔记和记忆到 GitHub！
> ```powershell
> # 同步笔记
> cd D:\网安
> git add .
> git commit -m "描述今天做了什么"
> git push
> 
> # 如果有新记忆，也要更新 .claude-memory/
> Copy-Item "$env:USERPROFILE\.claude\projects\C--Users-Administrator\memory\*.md" "D:\网安\.claude-memory\" -Force
> ```

如果用户让我直接执行同步，就直接跑命令。

**相关记忆：** [[notion-to-obsidian-migration]] [[week2-thursday-peft-progress]]
