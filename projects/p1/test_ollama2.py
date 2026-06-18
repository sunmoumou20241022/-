"""测试 Ollama 的原生 /api/chat 接口"""
import requests
import json

url = "http://localhost:11434/api/chat"
body = {
    "model": "llama3.2:3b",
    "messages": [
        {"role": "system", "content": "You are a cooking assistant."},
        {"role": "user", "content": "What is a good pasta recipe?"}
    ],
    "stream": False
}

print("正在测试 /api/chat 接口...")
try:
    r = requests.post(url, json=body, timeout=120)
    print(f"状态码: {r.status_code}")
    print(f"回复: {r.text[:500]}")
except Exception as e:
    print(f"错误: {e}")
