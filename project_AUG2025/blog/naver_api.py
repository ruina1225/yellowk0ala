# naver_api.py
# 네이버 토큰 재발급 + 블로그 업로드 
import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("NAVER_REFRESH_TOKEN")
FALLBACK_ACCESS = os.getenv("NAVER_ACCESS_TOKEN")  # 선택: 임시 토큰
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
BLOG_WRITE_URL = "https://openapi.naver.com/blog/writePost.json"

class NaverAuthError(Exception):
    """네이버 인증 관련 오류"""

class NaverApiError(Exception):
    """네이버 API 호출 실패"""


def _refresh_access_token() -> str:
    """
    refresh_token으로 access_token 재발급. 구성 없으면 FALLBACK_ACCESS로 시도.
    """
    if not (CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN):
        if FALLBACK_ACCESS:
            return FALLBACK_ACCESS
        raise NaverAuthError("NAVER OAuth env 부족: NAVER_CLIENT_ID/SECRET/REFRESH_TOKEN 필요")

    params = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
    }
    r = requests.get(TOKEN_URL, params=params, timeout=15)
    data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text}
    token = data.get("access_token")
    if not token:
        raise NaverAuthError(f"토큰 재발급 실패: {data}")
    return token


def write_blog_post(title: str, contents: str, category_no: Optional[int] = None) -> Dict[str, Any]:
    """
    DRY_RUN=true면 실제 업로드 대신 페이로드만 반환.
    성공/실패 응답 JSON 그대로 반환. 실패 판단은 message 필드 확인 권장.
    """
    payload = {"title": title, "contents": contents}
    if category_no is not None:
        payload["categoryNo"] = str(category_no)

    if DRY_RUN:
        return {"dry_run": True, "endpoint": BLOG_WRITE_URL, "payload": payload}

    access_token = _refresh_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.post(BLOG_WRITE_URL, headers=headers, data=payload, timeout=20)

    try:
        data = r.json()
    except Exception:
        data = {"error": "invalid_json", "raw": r.text[:800]}

    # 네이버는 실패도 200을 줄 수 있음 → message 검사
    if isinstance(data, dict) and data.get("message") != "success":
        raise NaverApiError(f"블로그 업로드 실패: {data}")
    return data

