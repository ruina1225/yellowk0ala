# queue_file.py
import json, shutil, time
from pathlib import Path
from typing import Optional, Tuple, Dict

# 실행 위치와 무관하게 같은 폴더를 보게 고정
ROOT = Path(__file__).resolve().parent
BASE = ROOT / "queue"
INBOX = BASE / "inbox"
PROCESSING = BASE / "processing"
DONE = BASE / "done"
FAILED = BASE / "failed"

def ensure_dirs():
    for p in [INBOX, PROCESSING, DONE, FAILED]:
        p.mkdir(parents=True, exist_ok=True)

def _oldest_json(directory: Path) -> Optional[Path]:
    files = sorted(directory.glob("*.json"), key=lambda p: p.stat().st_mtime)
    files = [f for f in files if f.stat().st_size > 0]  # 빈 파일 스킵
    return files[0] if files else None

def _move_to_failed(path: Path, reason: str):
    FAILED.mkdir(parents=True, exist_ok=True)
    try:
        raw = path.read_text(encoding="utf-8-sig", errors="ignore")
        try:
            data = json.loads(raw)
        except Exception:
            data = {"_corrupted": True, "_raw_snippet": raw[:200]}
        data["_error"] = reason
        (FAILED / path.name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    finally:
        path.unlink(missing_ok=True)

def dequeue() -> Tuple[Optional[Dict], Optional[Path]]:
    ensure_dirs()
    while True:
        src = _oldest_json(INBOX)
        if not src:
            return None, None
        ts = int(time.time() * 1000)
        dst = PROCESSING / f"{src.stem}__{ts}.json"
        shutil.move(str(src), str(dst))
        try:
            text = dst.read_text(encoding="utf-8-sig")  # ★ BOM 허용
            data = json.loads(text)
            # 표준화: processing 파일은 BOM 없는 UTF-8로 다시 저장
            dst.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return data, dst
        except Exception as e:
            _move_to_failed(dst, f"JSON 파싱 실패(dequeue): {e}")

def mark_done(proc_path: Path, extra: Optional[Dict] = None):
    ensure_dirs()
    text = proc_path.read_text(encoding="utf-8-sig")   # ★ BOM 허용
    try:
        data = json.loads(text)
    except Exception as e:
        _move_to_failed(proc_path, f"JSON 파싱 실패(mark_done): {e}")
        return
    if extra:
        data["_result"] = extra
    dst = DONE / proc_path.name
    dst.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    proc_path.unlink(missing_ok=True)

def mark_failed(proc_path: Path, reason: str):
    ensure_dirs()
    try:
        text = proc_path.read_text(encoding="utf-8-sig")
        data = json.loads(text)
    except Exception:
        raw = proc_path.read_text(encoding="utf-8-sig", errors="ignore")
        data = {"_corrupted": True, "_raw_snippet": raw[:200]}
    data["_error"] = reason
    dst = FAILED / proc_path.name
    dst.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    proc_path.unlink(missing_ok=True)


# # queue_file.py
# # 파일 기반 큐 유틸리티: enqueue / dequeue / mark_done / mark_failed
# # data/ 하위 파일을 사용: urls.txt (대기열), processed.txt (완료), failed.log (실패로그), state.json (재시도 카운트)

# from pathlib import Path  # 경로/파일 조작 편의
# import json               # state.json 읽기/쓰기
# from typing import Optional  # 함수 반환 타입 힌트

# DATA_DIR = Path("data")                         # 데이터 폴더 경로
# PENDING_FILE = DATA_DIR / "urls.txt"            # 대기열 파일
# PROCESSED_FILE = DATA_DIR / "processed.txt"     # 완료 누적 파일
# FAILED_LOG = DATA_DIR / "failed.log"            # 실패 로그 파일
# STATE_FILE = DATA_DIR / "state.json"            # 재시도 횟수/중복 방지용 상태 파일

# def _ensure_files() -> None:
#     """필요한 폴더/파일이 없으면 생성"""
#     DATA_DIR.mkdir(parents=True, exist_ok=True)                         # data/ 폴더 생성
#     for f in [PENDING_FILE, PROCESSED_FILE, FAILED_LOG]:                # 주요 파일들 순회
#         if not f.exists():                                              # 없으면
#             f.write_text("", encoding="utf-8")                          # 빈 파일로 생성
#     if not STATE_FILE.exists():                                         # state.json 없으면
#         STATE_FILE.write_text(json.dumps({"retries": {}}, ensure_ascii=False, indent=2), encoding="utf-8")

# def enqueue(url: str) -> bool:
#     """큐에 URL 추가. 이미 처리/대기 중이면 False."""
#     _ensure_files()                                                     # 파일 보장
#     url = url.strip()                                                   # 좌우 공백 제거
#     if not url:                                                         # 빈 문자열 금지
#         return False
#     # 중복 방지: 이미 processed.txt 또는 urls.txt에 있으면 스킵
#     if url in PROCESSED_FILE.read_text(encoding="utf-8").splitlines():  # 완료된 항목에 존재?
#         return False
#     if url in PENDING_FILE.read_text(encoding="utf-8").splitlines():    # 대기열에 이미 존재?
#         return False
#     with PENDING_FILE.open("a", encoding="utf-8") as f:                 # append 모드
#         f.write(url + "\n")                                             # 한 줄 추가
#     return True

# def dequeue() -> Optional[str]:
#     """대기열 맨 앞을 꺼내 반환. 없으면 None."""
#     _ensure_files()                                                     # 파일 보장
#     lines = PENDING_FILE.read_text(encoding="utf-8").splitlines()       # 전체 읽기
#     if not lines:                                                       # 비어있으면
#         return None
#     url = lines[0]                                                      # 첫 줄 선택
#     # 첫 줄 제거 후 저장
#     PENDING_FILE.write_text("\n".join(lines[1:]) + ("\n" if len(lines) > 1 else ""), encoding="utf-8")
#     return url

# def mark_done(url: str) -> None:
#     """처리 완료로 기록"""
#     _ensure_files()                                                     # 파일 보장
#     with PROCESSED_FILE.open("a", encoding="utf-8") as f:               # 완료 파일 append
#         f.write(url + "\n")                                             # 기록
#     # 성공시 재시도 카운트는 리셋
#     state = json.loads(STATE_FILE.read_text(encoding="utf-8"))          # state 로드
#     state.get("retries", {}).pop(url, None)                             # 해당 url 항목 제거
#     STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

# def mark_failed(url: str, reason: str, max_retry: int = 3) -> bool:
#     """
#     실패 기록 + 재시도 관리.
#     반환값: True면 재시도 대상(큐 재적재), False면 재시도 한도 초과.
#     """
#     _ensure_files()                                                     # 파일 보장
#     # 실패 로그 남기기
#     with FAILED_LOG.open("a", encoding="utf-8") as f:                   # 실패 로그 append
#         f.write(f"{url}\t{reason}\n")                                   # 탭 구분 기록
#     # 재시도 카운트 증가
#     state = json.loads(STATE_FILE.read_text(encoding="utf-8"))          # state 로드
#     retries = state.setdefault("retries", {})                           # 딕셔너리 보장
#     count = retries.get(url, 0) + 1                                     # 카운트 +1
#     retries[url] = count                                                # 업데이트
#     STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
#     # 재시도 남았으면 큐에 다시 넣기
#     if count < max_retry:                                               # 최대 재시도 미만?
#         with PENDING_FILE.open("a", encoding="utf-8") as f:             # 대기열 append
#             f.write(url + "\n")                                         # 재적재
#         return True                                                     # 재시도 예정
#     return False                                                        # 한도 초과
