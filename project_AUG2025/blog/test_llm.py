import requests

resp = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:7b-instruct",
        "prompt": "골프 여행 블로그 글 한 문장 예시",
        "stream": False  # ★ 꼭 추가!
    }
)

data = resp.json()
print(data["response"])  # 정상적으로 한 문장 출력됨
