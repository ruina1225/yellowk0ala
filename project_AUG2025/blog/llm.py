# llm.py
# 간단 버전 (timeout=300, 프록시 무시 적용)

import os
import requests
from dotenv import load_dotenv

print("[llm.py] loaded v2 (timeout=300, no proxies)")  # 버전 표식

load_dotenv()

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")


def run_llm_transform(raw_text: str) -> str:
    """
    Ollama generate API (non-stream) 호출.
    - timeout을 넉넉하게(300초) 설정
    - 프록시 무시 (기업망/시스템 프록시 문제 회피)
    - JSON 응답 없을 시 원문 반환
    """
    url = f"{OLLAMA_BASE}/api/generate"
    prompt = (
        "다음 내용을 네이버 블로그에 맞춰 깔끔한 HTML로 정리해줘. "
        "서론/본문/정리 구조, 소제목 포함, 불필요한 수사는 줄이고 핵심 정보 위주로.\n\n"
        f"원문:\n{raw_text}"
    )

    try:
        resp = requests.post(
            url,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=300,                               # ← 5분 (모델 로딩 대비)
            proxies={"http": None, "https": None},     # ← 프록시 무시
        )
        resp.raise_for_status()
        if resp.headers.get("content-type", "").startswith("application/json"):
            data = resp.json()
            return data.get("response", raw_text)
        return raw_text
    except requests.exceptions.Timeout:
        return "[ERROR] Ollama 요청이 시간 초과되었습니다."
    except Exception as e:
        return f"[ERROR] Ollama 호출 실패: {e}"






# # llm.py
# # Ollama /api/generate 호출로 요약/재작성 수행
# # 포인트: stream=False를 사용해 응답 본문을 "한 번에" 받아 JSON 디코딩 오류(Extra data) 회피

# import os                            # 환경변수
# import requests                      # HTTP 요청
# from dotenv import load_dotenv       # .env 로딩

# load_dotenv()                        # .env 읽기
# OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11434")  # Ollama 베이스 URL
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")   # 모델 이름

# def generate_rewrite(title: str, text: str, locks: dict) -> str:
#     """
#     원문 요약 + 잠금(가격/기간/날짜)을 반영해 블로그용 재작성
#     반환: 재작성된 본문(마크다운/HTML 혼용 가능)
#     """
#     # 시스템/유저 프롬프트 구성
#     system = (
#         "당신은 여행사 블로그 글 재작성 전문가입니다. "
#         "사용자 잠금(가격, 기간, 날짜)을 변경하지 말고, 누락되었다면 자연스럽게 문장에 포함하세요. "
#         "SEO를 고려해 소제목과 불릿을 적절히 사용하세요."
#     )
#     user = (
#         f"[제목]\n{title}\n\n"
#         f"[원문]\n{text[:4000]}\n\n"  # 너무 길면 모델 부담 → 앞부분만 사용(필요시 요약 단계를 추가)
#         f"[잠금]\n{locks}"
#     )
#     # Ollama /api/generate 호출 페이로드
#     payload = {
#         "model": OLLAMA_MODEL,   # 사용할 모델
#         "prompt": f"System: {system}\n\nUser: {user}\n\nAssistant:",  # 단순 프롬프트(지시 + 콘텍스트)
#         "stream": False          # 스트리밍 비활성화(한 번에 JSON)
#     }
#     # 요청
#     resp = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=120)  # 타임아웃
#     resp.raise_for_status()      # 오류코드 예외
#     data = resp.json()           # JSON 디코드(스트리밍X라 안전)
#     # Ollama generate 응답의 핵심 출력은 "response" 필드
#     return data.get("response", "").strip()
