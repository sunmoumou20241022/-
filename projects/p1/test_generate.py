"""测试 Ollama /api/generate 接口"""
import requests
import json
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = "http://localhost:11434/api/generate"

# 测试 1：简单问题
print("=== 测试 /api/generate ===")
body = {
    "model": "llama3.2:3b",
    "prompt": "What is a good pasta recipe? Keep it short.",
    "stream": False
}
try:
    r = requests.post(url, json=body, timeout=60)
    data = r.json()
    print(f"状态码: {r.status_code}")
    print(f"回复: {data.get('response', '')[:300]}")
    print(f"总耗时: {data.get('total_duration', 0) / 1e9:.1f}秒")
except Exception as e:
    print(f"错误: {e}")

# 测试 2：带 system prompt
print("\n=== 测试带 system prompt ===")
body2 = {
    "model": "llama3.2:3b",
    "system": "You are a cooking assistant named Chef Claude. You only answer cooking questions.",
    "prompt": "What is the capital of France?",
    "stream": False
}
try:
    r2 = requests.post(url, json=body2, timeout=60)
    data2 = r2.json()
    print(f"回复: {data2.get('response', '')[:300]}")
except Exception as e:
    print(f"错误: {e}")

# 测试 3：用 8b 模型
print("\n=== 测试 llama3.1:8b ===")
body3 = {
    "model": "llama3.1:8b",
    "prompt": "What is a good pasta recipe? Keep it short.",
    "stream": False
}
try:
    r3 = requests.post(url, json=body3, timeout=120)
    data3 = r3.json()
    print(f"回复: {data3.get('response', '')[:300]}")
    print(f"总耗时: {data3.get('total_duration', 0) / 1e9:.1f}秒")
except Exception as e:
    print(f"错误: {e}")
