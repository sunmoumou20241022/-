# Ollama 底层架构与部署逻辑

# Ollama 极简版本 Payload (Windows 极速部署)

## Step 1: 安装引擎

双击运行下载好的 `OllamaSetup.exe`，默认安装，无需任何配置。

## Step 2: 拉取并运行模型

打开 CMD 终端，执行以下命令拉取通义千问 2.5（7B 参数量版本）：

```
ollama run qwen2.5:7b
(注：首次执行会自动下载约 4.7GB 的权重文件，出现 >>> 提示符即代表启动成功。按 Ctrl+D 退出终端对话，引擎将转入后台静默运行。)
```

## Step 3: Python 接口直连 (Notion 隐形助理核心代码)

新建 `.py` 文件，写入以下极简直连代码即可实现本地算力调度：

```python
import requests
import pyperclip

URL = "<http://127.0.0.1:11434/api/generate>"

def process_clipboard():
    raw_text = pyperclip.paste()
    if not raw_text.strip(): return

    print("[*] 正在呼叫本地算力 (Qwen 2.5)...")
    payload = {
        "model": "qwen2.5:7b",
        "prompt": "作为网安助理，请用 Markdown 极客排版重构以下草稿：\\n" + raw_text,
        "stream": False
    }

    try:
        response = requests.post(URL, json=payload, timeout=120).json()
        pyperclip.copy(response['response'])
        print("[+] 本地注入成功！请在 Notion 粘贴 (Ctrl+V)。")
    except Exception as e:
        print(f"[-] 本地接口调用失败: {e}")

keyboard.add_hotkey('ctrl+alt+g', process_clipboard)
keyboard.wait()
```

### 必要解释极简版原理

### 因为 Ollama 的安装包自带了预编译的硬件加速驱动，它会自动探测你的电脑是 CPU 还是 GPU 跑得快。而 Python 代码之所以能精简到这个地步，是因为所有的通信都发生在 127.0.0.1 物理机内部，彻底绕过了 GFW、云端风控（403）、API 配额（429）以及 HTTPS 证书校验。这就是“纯本地纯明文”带来的极致暴力美学。

### 【省力替代方案】

在未来的网安实战中，如果你在 Kali Linux 虚拟机里打靶场，遇到一段极度复杂的混淆代码或 Base64 嵌套加密，连 Python 脚本都不用写。只要你的 Windows 宿主机开着 Ollama，在 Kali 的终端里直接用 curl 结合 jq，一行命令就能让宿主机的 AI 帮你完成代码审计：

```bash
# 假设你 Windows 宿主机的局域网 IP 是 192.168.1.100
curl -s -X POST <http://192.168.1.100:11434/api/generate> -d '{"model":"qwen2.5:7b", "prompt":"解释这段恶意 Payload 的原理：<你的Payload>", "stream":false}' | jq -r '.response'
```

这行代码会像一把尖刀一样直插本地 API，瞬间把大模型的审计结果格式化输出在你的 Kali 终端屏幕上！