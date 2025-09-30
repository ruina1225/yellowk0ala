# scrape.py
# URL의 HTML을 내려받아 제목/본문 텍스트/이미지 URL들을 추출
# (네이버 블로그 등 구조가 다양하므로, 우선 "일반적인 기사/블로그" 패턴을 커버하는 기본기)

import requests                         # HTTP 요청
from bs4 import BeautifulSoup           # HTML 파싱
from urllib.parse import urljoin        # 상대경로 → 절대경로 변환

def fetch_and_parse(url: str) -> BeautifulSoup:
    """URL에서 HTML 가져와 BeautifulSoup 객체 반환"""
    headers = {"User-Agent": "Mozilla/5.0 (naver-golf-bot)"}  # 간단한 UA
    resp = requests.get(url, headers=headers, timeout=20)     # 타임아웃 20초
    resp.raise_for_status()                                   # 4xx/5xx 예외
    # 일부 블로그는 'lxml' 파서가 좀 더 안정적
    return BeautifulSoup(resp.text, "lxml")                   # soup 생성

def extract_content(url: str) -> dict:
    """
    제목(title), 본문 텍스트(text), 이미지 목록(images) 추출.
    반환: {"title": str, "text": str, "images": [str]}
    """
    soup = fetch_and_parse(url)                               # soup 확보
    # 제목 후보: <title> 또는 h1/h2
    title = (soup.title.string.strip() if soup.title and soup.title.string else "").strip()
    if not title:                                             # <title> 없을 경우
        h1 = soup.find("h1")                                  # h1 우선
        title = (h1.get_text(strip=True) if h1 else "")
    # 본문 후보: article 태그 또는 div[class*=content|post]
    article = soup.find("article")                            # <article> 우선
    if not article:                                           # 없으면
        article = soup.find("div", class_=lambda c: c and any(k in c.lower() for k in ["content", "post", "article"]))
    # 텍스트 추출: p 태그 기반
    paragraphs = []
    if article:                                               # 후보 영역이 있으면
        for p in article.find_all("p"):                       # 모든 p 순회
            txt = p.get_text(" ", strip=True)                 # p 텍스트 수집
            if txt:
                paragraphs.append(txt)                        # 비어있지 않으면 추가
    text = "\n".join(paragraphs)                              # 줄바꿈으로 합치기
    # 이미지 src 모으기
    images = []
    for img in (article or soup).find_all("img"):             # 기사 내부 우선, 없으면 전체
        src = img.get("src") or img.get("data-src")           # 지연 로딩 케이스 고려
        if src:
            images.append(urljoin(url, src))                  # 절대경로화
    # 결과 반환
    return {"title": title, "text": text, "images": images}
