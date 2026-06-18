"""快速测试 Ollama 连接"""
import requests
import json

url = "http://localhost:11434/v1/chat/completions"
body = {
    "model": "llama3.2:3b",
    "messages": [
        {"role": "system", "content": "You are a cooking assistant."},
        {"role": "user", "content": "What is a good pasta recipe?"}
    ],
    "temperature": 0
}

print("正在连接 Ollama...")
try:
    r = requests.post(url, json=body, timeout=120)
    print(f"状态码: {r.status_code}")
    print(f"回复: {r.text[:500]}")
except Exception as e:
    print(f"错误: {e}")
