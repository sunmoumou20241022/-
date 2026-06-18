"""测试 Ollama 原生接口（修复编码）"""
import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 先试 /api/chat（原生接口）
url = "http://localhost:11434/api/chat"
body = {
    "model": "llama3.2:3b",
    "messages": [
        {"role": "system", "content": "You are a cooking assistant."},
        {"role": "user", "content": "What is a good pasta recipe?"}
    ],
    "stream": False
}

print("=== 测试 /api/chat（原生接口）===")
try:
    r = requests.post(url, json=body, timeout=120)
    print(f"状态码: {r.status_code}")
    data = r.json()
    print(f"回复: {data.get('message', {}).get('content', '')[:200]}")
    print("✅ 原生接口 OK")
except Exception as e:
    print(f"❌ 原生接口失败: {e}")

# 再试 /v1/chat/completions（OpenAI 兼容接口）
print("\n=== 测试 /v1/chat/completions（OpenAI 兼容接口）===")
url2 = "http://localhost:11434/v1/chat/completions"
body2 = {
    "model": "llama3.2:3b",
    "messages": [
        {"role": "system", "content": "You are a cooking assistant."},
        {"role": "user", "content": "What is a good pasta recipe?"}
    ],
    "temperature": 0
}
try:
    r2 = requests.post(url2, json=body2, timeout=120)
    print(f"状态码: {r2.status_code}")
    data2 = r2.json()
    print(f"回复: {data2.get('choices', [{}])[0].get('message', {}).get('content', '')[:200]}")
    print("✅ OpenAI 兼容接口 OK")
except Exception as e:
    print(f"❌ OpenAI 兼容接口失败: {e}")
