# Notion 笔记迁移到 Obsidian

以后如果还有 Notion 笔记要迁移，按这个流程操作。

## 1. Notion 导出

1. 打开 Notion，进入要导出的**最顶层页面**
2. 右上角 `⋯` → **Export**
3. 设置：
   - **Format**: `Markdown & CSV`
   - ✅ **Include sub-pages**（必须勾选！否则子页面不会导出）
   - ✅ **Create folders for subpages**
   - ✅ **Include attached files**
4. 点击 Export，下载 ZIP 文件

> ⚠️ 下载的是**双层 ZIP**，需要解压两次才能看到 .md 文件。

## 2. 解压

```powershell
# 第一次解压
Expand-Archive -Path "下载的文件.zip" -DestinationPath "C:\Users\Administrator\Desktop\export1" -Force

# 里面还有一个 ExportBlock-xxx.zip，再解压一次
Expand-Archive -Path "C:\Users\Administrator\Desktop\export1\ExportBlock-*\*.zip" -DestinationPath "C:\Users\Administrator\Desktop\export1\unpacked" -Force
```

## 3. 运行清洗脚本

```powershell
python C:\Users\Administrator\notion_to_obsidian.py "C:\Users\Administrator\Desktop\export1\unpacked" "D:\网安\网安\从Notion导入"
```

脚本会自动处理：
- 去掉文件名中的 UUID 后缀
- Notion 内部链接 → Obsidian 双链 `[[标题]]`
- 图片路径 URL 编码 → 中文解码
- 去掉图片 alt 的 `.json` 后缀
- 压缩多余空行
- 复制图片和附件

## 4. 复制到 Vault

把清洗后的笔记从 `从Notion导入/` 移到 Vault 对应的文件夹里：

```powershell
# 比如导入的笔记叫"网络协议"
Copy-Item "D:\网安\网安\从Notion导入\网络协议" -Destination "D:\网安\网安\网络协议" -Recurse -Force
Copy-Item "D:\网安\网安\从Notion导入\网络协议.md" -Destination "D:\网安\网安\网络协议.md" -Force
```

## 5. 同步到 GitHub

```powershell
cd D:\网安
git add .
git commit -m "从 Notion 导入 xxx 笔记"
git push
```

## 6. 清理临时文件

```powershell
Remove-Item "D:\网安\网安\从Notion导入" -Recurse -Force
Remove-Item "C:\Users\Administrator\Desktop\export1" -Recurse -Force
```

---

## 注意事项

- **数据库/表格**：Notion 导出为 CSV，Obsidian 不直接支持，需要手动整理成 Markdown 表格
- **嵌入块**：Notion 的 embed 可能丢失，需要重新链接
- **公式**：大部分兼容，复杂 LaTeX 可能需要微调
- **先小批量试**：建议先导出一个子页面试试，确认效果满意后再全量导出
