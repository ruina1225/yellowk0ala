# post_naver.py
# 네이버 블로그 API 업로드(개념 예시). DRY_RUN=true면 실제 업로드 대신 저장/출력.

import os                            # 환경변수
import requests                      # HTTP 요청
from pathlib import Path             # 파일 저장
from dotenv import load_dotenv       # .env 로딩
from typing import List              # 타입 힌트
import uuid                          # 임시 파일명 등

load_dotenv()                        # .env 로딩
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"  # 드라이런 여부
NAVER_ACCESS_TOKEN = os.getenv("NAVER_ACCESS_TOKEN")      # 네이버 액세스 토큰
NAVER_BLOG_ID = os.getenv("NAVER_BLOG_ID")                # 블로그 ID
OUT_DIR = Path("data/out")                                # 프리뷰/산출물 저장 폴더
OUT_DIR.mkdir(parents=True, exist_ok=True)                # 폴더 보장

def _download_images(image_urls: List[str]) -> List[Path]:
    """이미지 URL들을 로컬에 다운로드하여 파일 경로 목록 반환"""
    saved = []                                                  # 저장 경로 리스트
    for url in image_urls[:5]:                                  # 과도한 다운로드 방지(최대 5장)
        try:
            r = requests.get(url, timeout=20)                   # 이미지 요청
            r.raise_for_status()                                # 4xx/5xx 예외
            ext = ".jpg"                                        # 간단히 jpg로 저장(실제는 Content-Type 판단)
            path = OUT_DIR / f"{uuid.uuid4().hex}{ext}"         # 임의 파일명
            path.write_bytes(r.content)                         # 바이너리 저장
            saved.append(path)                                  # 리스트에 추가
        except Exception:
            # 다운로드 실패는 치명적이지 않으므로 무시(필요시 로그)
            pass
    return saved                                                # 저장된 경로 목록

def upload_post(title: str, html_body: str, image_urls: List[str]) -> dict:
    """
    네이버 블로그 업로드(개념).
    반환: {"ok": bool, "post_id": str | None, "preview_path": str | None}
    """
    # 프리뷰 파일 저장(디버깅/검수용)
    preview_path = OUT_DIR / f"preview_{uuid.uuid4().hex}.html"         # 프리뷰 파일 경로
    preview_html = f"<h1>{title}</h1>\n{html_body}"                     # 간단한 프리뷰
    preview_path.write_text(preview_html, encoding="utf-8")             # 저장

    if DRY_RUN:
        # 실제 업로드 대신 프리뷰 경로만 반환
        print(f"[DRY_RUN] 제목: {title}\n미리보기: {preview_path}")
        return {"ok": True, "post_id": None, "preview_path": str(preview_path)}

    # 실제 업로드 로직(예시: 멀티파트로 이미지 업로드 후 본문에 이미지 삽입)
    # 네이버 API 스펙에 맞춰 엔드포인트/필드를 맞추세요.
    if not (NAVER_ACCESS_TOKEN and NAVER_BLOG_ID):
        return {"ok": False, "post_id": None, "preview_path": str(preview_path), "error": "NAVER creds missing"}

    # 1) 이미지 업로드 (실제 스펙에 맞춰 구현 필요)
    uploaded_image_urls = []                                            # API 업로드 후 반환된 URL들
    image_paths = _download_images(image_urls)                          # 먼저 로컬에 다운
    for p in image_paths:                                               # 각 파일 업로드
        # TODO: 네이버 이미지 업로드 API 호출 (예시 자리)
        # res = requests.post(NAVER_IMAGE_UPLOAD_URL, headers=..., files={"image": open(p,"rb")}, data=...)
        # uploaded_image_urls.append(res.json()["url"])
        uploaded_image_urls.append(f"file://{p}")                       # 데모: 로컬 경로를 가짜 URL로 사용

    # 2) 본문에 이미지 태그 삽입(간단)
    for u in uploaded_image_urls:                                       # 업로드된 URL들을
        html_body += f'\n<p><img src="{u}" alt=""/></p>'                # 끝에 삽입

    # 3) 글쓰기 API 호출 (예시 자리 — 실제 엔드포인트/파라미터 교체)
    try:
        # res = requests.post(NAVER_WRITE_URL, headers={"Authorization": f"Bearer {NAVER_ACCESS_TOKEN}"}, data={
        #     "blogId": NAVER_BLOG_ID,
        #     "title": title,
        #     "content": html_body,
        # })
        # res.raise_for_status()
        # post_id = res.json().get("postId")
        post_id = "DEMO_POST_ID"                                        # 데모용
        return {"ok": True, "post_id": post_id, "preview_path": str(preview_path)}
    except Exception as e:
        return {"ok": False, "post_id": None, "preview_path": str(preview_path), "error": str(e)}
