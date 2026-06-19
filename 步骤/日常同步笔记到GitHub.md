# 日常同步笔记到 GitHub

每天写完笔记后，运行以下命令同步：

```powershell
cd D:\网安
git add .
git commit -m "更新笔记"
git push
```

> commit 信息可以随便写，写个大概就行，比如"6月20日笔记"、"添加xx笔记"。

---

## Token 说明

- Git 推送时使用的是保存在本地的 GitHub Personal Access Token
- 如果 Token 过期，推送会报认证错误，需要重新生成：
  1. 去 GitHub → Settings → Developer settings → Personal access tokens
  2. 生成新 Token（勾选 repo 权限）
  3. 运行 `git remote set-url origin https://<新Token>@github.com/sunmoumou20241022/-.git`

## 仓库信息

- **地址**：https://github.com/sunmoumou20241022/-
- **类型**：私有仓库（只有自己能看）
