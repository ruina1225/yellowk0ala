# feed_watcher_file.py
# RSS 피드에서 새 글을 찾아 data/urls.txt 큐에 넣기
# state.json에 마지막으로 본 entry ID를 저장해 중복 방지

import feedparser                    # RSS 파서
import json                          # state 저장/로드
from pathlib import Path             # 파일 경로
from typing import List              # 타입 힌트
from queue_file import enqueue       # 큐에 넣기

STATE_FILE = Path("data/state.json") # 상태 파일 경로 (queue_file와 공유)

def _load_state() -> dict:
    """state.json 로드(없으면 기본값)"""
    if STATE_FILE.exists():                                  # 파일 존재?
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))  # 로드
    return {"retries": {}, "feeds": {}}                      # 기본 상태

def _save_state(state: dict) -> None:
    """state.json 저장"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)     # 경로 보장
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def watch_feed(feed_url: str, limit: int = 10) -> int:
    """
    RSS feed_url에서 최신 글 최대 limit개를 읽어 큐에 적재.
    반환: 새로 적재한 URL 개수
    """
    d = feedparser.parse(feed_url)                           # 피드 파싱
    state = _load_state()                                    # 상태 로드
    feeds_state = state.setdefault("feeds", {})              # feed 상태 dict 보장
    last_id = feeds_state.get(feed_url)                      # 마지막으로 본 entry ID
    new_count = 0                                            # 적재 수 카운트

    for entry in d.entries[:limit]:                          # 최신 limit개 순회
        entry_id = entry.get("id") or entry.get("link")      # ID가 없으면 링크로 대체
        if entry_id == last_id:                              # 마지막 본 항목 도달?
            break                                            # 이후는 예전 글이므로 중단
        url = entry.get("link")                              # 본문 링크
        if url and enqueue(url):                             # 큐 적재 성공 시
            new_count += 1                                   # 카운트 +1

    if d.entries:                                            # 엔트리가 있다면
        newest = d.entries[0]                                # 가장 최신
        feeds_state[feed_url] = newest.get("id") or newest.get("link")  # 최신 ID 저장

    _save_state(state)                                       # 상태 저장
    return new_count                                         # 적재 개수 반환
